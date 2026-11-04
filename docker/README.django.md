# EC2 배포: Django 로그인 + RDS MySQL 8.4 + 기존 AI API

`docker-compose.web.yml`은 로그인 기능이 있는 `web/`을 배포합니다. 기존 `docker-compose.yml`의 Streamlit 화면과는 별도 진입점이며, 두 구성은 같은 `beaurette` 프로젝트의 API 서비스를 재사용합니다.

```text
브라우저 → Caddy(HTTPS·정적 파일) → Django/Gunicorn → RDS MySQL 8.4
                                      └→ FastAPI → OpenAI / Qdrant Cloud
```

- 회원가입·로그인·로그아웃은 기존 Django 기능을 사용합니다. 아이디(username) + 비밀번호 방식입니다.
- `migrate`가 `auth_user`, `django_session`, 제품·실증·검토·생성·채팅 테이블을 생성합니다. 별도 `USER` 테이블을 수동 생성하지 않습니다.
- 루트 `.env`는 기존 API의 OpenAI/Qdrant 설정, `web/.env`는 Django/RDS 설정입니다. 프록시에는 DB 비밀번호나 API 키를 전달하지 않습니다.
- 이미지 빌드는 고정된 `web/uv.lock`을 사용하고 정적 파일을 수집합니다. DB 연결, 마이그레이션, 유료 AI 호출은 빌드에 포함하지 않습니다.
- 운영 환경에서 DB 설정이 없거나 SQLite를 지정하면 기동을 거부합니다. 컨테이너 내부 파일에 회원 정보가 저장되는 실수를 방지합니다.

## 1. RDS 준비

1. EC2와 같은 리전·VPC에 **RDS MySQL 8.4**을 생성합니다. 처음부터 RDS의 인스턴스 식별자와 별도로 실제 데이터베이스 `beaurette`도 준비합니다.
2. 퍼블릭 액세스는 사용하지 않습니다. RDS 보안 그룹의 MySQL/Aurora TCP `3306` 소스에는 **EC2에 연결된 보안 그룹 ID**를 지정합니다.
3. `beaurette` DB의 앱 전용 계정을 준비합니다. 이 계정에는 초기 마이그레이션을 위한 해당 DB 스키마의 생성·변경 권한이 필요합니다. RDS 관리자 계정과 구분해 관리합니다.
4. RDS 엔드포인트, DB 이름, 사용자, 비밀번호를 서버의 `web/.env`에 입력합니다. 연결에는 엔드포인트 호스트명을 사용합니다.

이 가이드는 RDS를 자동으로 생성하거나 기존 DB를 변경하지 않습니다. AWS 인스턴스 비용은 선택한 RDS 구성에 따라 발생합니다.

### EC2에서 MySQL 관리자 접속과 앱 계정 준비

RDS 상태가 `Available`인지 확인한 뒤, **SSH로 접속한 Ubuntu EC2 터미널**에서 실행합니다. RDS 보안 그룹의 `3306` 소스는 EC2 보안 그룹이어야 합니다.

```bash
sudo apt-get update
sudo apt-get install -y mysql-client
mkdir -p "$HOME/.mysql"
curl --fail --show-error --location https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem -o "$HOME/.mysql/rds-global-bundle.pem"
mysql --host=YOUR_RDS_ENDPOINT --port=3306 --user=admin --password --connect-timeout=10 --ssl-mode=VERIFY_IDENTITY --ssl-ca="$HOME/.mysql/rds-global-bundle.pem"
```

`YOUR_RDS_ENDPOINT`를 RDS 엔드포인트로 바꿉니다. `admin`은 RDS 생성 시 정한 마스터 사용자명이며, 다르게 만들었다면 수정합니다. 비밀번호는 `Enter password:`에서 입력합니다.

`mysql>` 프롬프트에서 확인합니다.

```sql
SELECT VERSION();
SHOW DATABASES;
SHOW SESSION STATUS LIKE 'Ssl_cipher';
```

앱 DB와 전용 계정이 아직 없을 때 다음 SQL을 실행합니다. 비밀번호는 예제 문자열을 그대로 사용하지 말고 별도로 생성한 충분히 긴 값으로 바꿉니다. `'`와 `\`가 없는 영문·숫자 임의 문자열이면 SQL 입력 시 이스케이프가 필요 없습니다. 이미 존재하는 계정에는 `CREATE USER`를 반복하거나 비밀번호를 임의로 변경하지 않습니다.

```sql
CREATE DATABASE IF NOT EXISTS beaurette CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
CREATE USER 'beaurette_app'@'%' IDENTIFIED BY 'REPLACE_WITH_A_LONG_RANDOM_PASSWORD' REQUIRE SSL;
GRANT ALL PRIVILEGES ON beaurette.* TO 'beaurette_app'@'%';
EXIT;
```

`%`는 DB 계정이 연결을 허용할 호스트 범위이며, 네트워크 접근은 EC2 전용 보안 그룹으로 제한합니다. 권한은 `beaurette` DB에만 부여합니다. 회원용 `auth_user` 등 테이블은 아래 `migrate`가 생성합니다.

기존 PostgreSQL도 지원합니다. 해당 엔진을 유지할 때만 `postgresql://...:5432/beaurette`와 `5432` 보안 그룹 규칙을 사용하며, 운영 TLS 모드는 `verify-full`입니다.

## 2. EC2에서 설정 파일 준비

최신 배포 코드가 반영된 저장소 루트에서 실행합니다. 기존 서버 폴더명이 `beaurette~`라면 마지막 `~`까지 포함합니다.

```bash
cd '/home/ubuntu/beaurette~'
test -f web/.env || cp docker/web.env.example web/.env
chmod 600 web/.env
nano web/.env
```

`DJANGO_SECRET_KEY`에는 별도로 생성한 긴 임의 문자열을 입력합니다. 서버에서 다음 명령으로 생성할 수 있습니다. 출력은 공유하거나 Git에 올리지 않습니다.

```bash
python3 -c 'import secrets; print(secrets.token_urlsafe(64))'
```

처음에는 예제의 `SITE_ADDRESS=http://localhost`, `WEB_BIND_IP=127.0.0.1`, `DJANGO_HTTPS=False`를 유지합니다. HTTP 로그인 화면은 서버 루프백에서만 제공하고, 아래 SSH 터널로 확인합니다.

```dotenv
DJANGO_SECRET_KEY=직접_생성한_긴_임의_문자열
DATABASE_URL=mysql://beaurette_app:비밀번호@RDS_엔드포인트:3306/beaurette
```

사용자명·비밀번호에 `@`, `:`, `/`, `#`, `%` 등이 있으면 URL 인코딩해야 합니다. 일반 문자열을 명령행에 붙이지 않고, 다음 명령의 숨김 입력창에서 비밀번호를 입력해 변환할 수 있습니다. 출력도 비밀번호와 동일하게 취급합니다.

```bash
python3 -c 'import getpass; from urllib.parse import quote; print(quote(getpass.getpass("DB password: "), safe=""))'
```

이미지에는 AWS RDS CA 인증서가 포함됩니다. `DEBUG=False`에서는 `VERIFY_IDENTITY`로 인증서와 호스트명을 검증합니다. 로컬에서 RDS를 점검할 경우 `DATABASE_SSL_ROOT_CERT`에 로컬 CA 파일의 절대 경로를 지정하세요.

저장: **Ctrl+O → Enter → Ctrl+X**.

## 3. 빌드 → 연결 점검 → 테이블 생성

이 문서의 모든 Compose 명령은 `--env-file web/.env -f docker-compose.web.yml`을 사용합니다. 기존 루트 `.env`는 API 서비스의 `env_file`로 별도 로드됩니다.

```bash
sudo docker compose --env-file web/.env -f docker-compose.web.yml config --quiet
sudo docker compose --env-file web/.env -f docker-compose.web.yml build api web proxy
```

설정 출력에는 비밀번호가 포함될 수 있으므로 `config`는 `--quiet`과 함께 사용합니다.

먼저 **읽기 전용** 연결 검사를 실행합니다. 빈 DB에서 `Migrations pending`은 정상이며 이 단계에서는 테이블을 만들지 않습니다.

```bash
sudo docker compose --env-file web/.env -f docker-compose.web.yml run --rm --no-deps web python manage.py check_database --allow-unmigrated
```

`Database connection: OK`가 나온 뒤, 테이블을 생성합니다. 실패하면 서비스 시작 전에 오류를 해결합니다. 기존 운영 DB 갱신 시에는 백업과 적용할 변경을 먼저 확인하세요.

```bash
sudo docker compose --env-file web/.env -f docker-compose.web.yml run --rm --no-deps web python manage.py migrate --plan
sudo docker compose --env-file web/.env -f docker-compose.web.yml run --rm --no-deps web python manage.py migrate --noinput
sudo docker compose --env-file web/.env -f docker-compose.web.yml run --rm --no-deps web python manage.py check_database
```

마지막 결과가 `Migrations: OK`여야 합니다. 시작 시 마이그레이션을 자동 실행하지 않으므로 여러 컨테이너가 동시에 스키마를 변경하지 않습니다. 필요하면 `sqlmigrate auth 0001` 등으로 마이그레이션이 만드는 SQL을 확인할 수 있습니다.

## 4. 실행과 비공개 로그인 확인

```bash
sudo docker compose --env-file web/.env -f docker-compose.web.yml up -d --wait --wait-timeout 180
sudo docker compose --env-file web/.env -f docker-compose.web.yml ps
curl --fail http://localhost/health/ready/
```

`api`, `web`은 healthy, `proxy`는 실행 중이어야 합니다. `/health/ready/`는 DB 연결과 미적용 마이그레이션을 검사하며 실패하면 503을 반환합니다. 기존 `/health/`는 AI 상태 진단용이고, AI 오류를 HTTP 200 본문으로 보고하므로 readiness 대신 사용하지 않습니다.

기존 Streamlit `app` 컨테이너가 남아 있으면 orphan 경고가 표시될 수 있습니다. 새 구성에 포함되지 않은 컨테이너가 있다는 안내이며, 공개 전 5단계에서 해당 서비스를 중지합니다.

**내 PC의 새 PowerShell 창**에서 SSH 터널을 엽니다. 키 경로와 EC2 IP는 본인 값으로 바꾸세요.

```powershell
$ec2Key = "$env:USERPROFILE\Downloads\Beaurette_ec2.pem"
ssh -i "$ec2Key" -N -L 8080:127.0.0.1:80 ubuntu@16.184.19.224
```

이 창을 열어둔 채 브라우저에서 `http://localhost:8080`으로 접속합니다. 화면은 SSH 터널을 통해 EC2의 Django에서 제공됩니다.

1. 회원가입 후 로그인 상태가 되는지 확인합니다.
2. 로그아웃 후 같은 아이디·비밀번호로 다시 로그인합니다.
3. 제품을 등록하고 검토·챗봇 요청을 한 번 실행합니다. 실제 AI 호출에는 사용량 비용이 발생합니다.
4. Django 컨테이너를 재시작한 후 다시 로그인하여 제품·이력이 남는지 확인합니다.

다른 계정의 제품·이력이 보이지 않는지도 확인합니다. 기존 Streamlit의 세션 데이터나 로컬 SQLite 계정은 RDS로 자동 이전되지 않습니다.

## 5. 도메인과 HTTPS로 공개

1. EC2의 고정 공인 IP를 준비하고 도메인의 DNS A 레코드를 그 IP로 연결합니다. 잘못된 AAAA 레코드가 있다면 실제 IPv6 설정과 일치하도록 수정합니다.
2. EC2 보안 그룹에 외부 TCP `80`, `443`을 허용합니다. SSH `22`는 관리자 IP만, RDS `3306`는 EC2 보안 그룹만 허용합니다. Gunicorn `8001`은 Docker 밖으로 공개하지 않습니다.
3. `web/.env`에서 아래 예시를 **실제 도메인**으로 변경합니다.

```dotenv
SITE_ADDRESS=beaurette.example.com
WEB_BIND_IP=0.0.0.0
DJANGO_ALLOWED_HOSTS=beaurette.example.com,localhost,127.0.0.1
DJANGO_CSRF_TRUSTED_ORIGINS=https://beaurette.example.com
DJANGO_HTTPS=True
```

`SITE_ADDRESS`는 하나의 실제 호스트명으로 설정합니다. Caddy가 인증서를 자동 발급·갱신하고 HTTP를 HTTPS로 리다이렉트합니다. Django도 HTTPS 리다이렉트와 Secure 쿠키를 적용합니다. 인증서는 `caddy_data` 볼륨에 보관되므로 재배포 때 볼륨을 삭제하지 않습니다.

4. **공개 전 기존 로그인 없는 Streamlit 경로를 종료**합니다. 보안 그룹의 `8501` 인바운드 규칙도 제거합니다. 기존 Compose 파일로 다시 전체 `up`하면 Streamlit이 재시작되므로 운영에는 Django용 명령을 사용합니다.

```bash
sudo docker compose stop app
sudo docker compose --env-file web/.env -f docker-compose.web.yml up -d --wait --wait-timeout 180
sudo docker compose --env-file web/.env -f docker-compose.web.yml logs --tail=80 web proxy
```

5. `https://실제도메인`에서 새로 회원가입·로그인·로그아웃·제품/검토 이력 저장을 확인합니다. 주소창에서 HTTPS인지, CSS와 관리자 화면 정적 파일도 표시되는지 확인합니다.

## 6. 갱신과 문제 확인

새 코드 반영 후 `build web proxy`, `migrate --plan`, `migrate --noinput`, `up -d --wait` 순서로 적용합니다. 정적 파일은 프록시 이미지에 포함되므로 **web과 proxy를 함께 빌드**합니다. API 변경도 있으면 api를 함께 빌드합니다.

```bash
sudo docker compose --env-file web/.env -f docker-compose.web.yml exec web python manage.py check_database
sudo docker compose --env-file web/.env -f docker-compose.web.yml exec api python scripts/check_connections.py
sudo docker compose --env-file web/.env -f docker-compose.web.yml logs --tail=100 web proxy
```

- DB 연결 실패: RDS 상태·엔드포인트·DB 이름·계정 권한·EC2/RDS 보안 그룹을 확인합니다. TLS 검증을 끄지 않고 인증서와 엔드포인트를 확인합니다.
- web unhealthy: `check_database`로 접속 및 미적용 마이그레이션을 확인합니다.
- 400/CSRF 오류: 실제 접속 도메인과 `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`, `DJANGO_HTTPS`를 맞춥니다.
- HTTPS 발급 실패: DNS와 EC2의 80/443 접근, 다른 서비스의 포트 점유 여부를 확인합니다.
- 환경변수 변경은 `up -d`로 반영합니다. `restart`만으로는 새 값이 적용되지 않습니다.

참고: [Django 배포](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/), [RDS MySQL 8.4 TLS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ConnectToInstanceSSL.CLI.html), [Caddy 자동 HTTPS](https://caddyserver.com/docs/automatic-https).
