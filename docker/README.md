# AWS EC2 배포: FastAPI + Streamlit + 기존 Qdrant Cloud

> **회원가입·로그인·RDS를 포함한 Django 배포는 [Django/RDS 배포 가이드](README.django.md)를 사용하세요.** 이 문서는 기존 Streamlit 배포를 유지·점검할 때 사용합니다. 두 화면의 계정과 저장 방식은 다릅니다.

루트 `docker-compose.yml`이 기본 배포 설정입니다. EC2 한 대에 API와 화면을 실행하고, 기존 Qdrant Cloud 컬렉션을 그대로 조회합니다. RDS, 로컬 Qdrant, GPU는 이 구성에 필요하지 않습니다. 등록 제품과 대화는 현재처럼 Streamlit 세션에만 유지되므로 서버 재시작 후 복원되지 않습니다.

## 1. EC2 준비

- Linux EC2에 Docker Engine과 Docker Compose 플러그인 **2.20.0 이상**을 설치합니다. 아래 명령은 Docker 실행 권한이 있는 계정 기준입니다.
- 저장소를 EC2에 체크아웃하고 저장소 루트에서 실행합니다. 빌드에는 패키지 다운로드와 이미지 저장 공간이 필요합니다.
- 초기 접속 확인용 보안 그룹: TCP **8501**을 본인/팀의 접속 IP에 허용합니다. SSH를 사용한다면 TCP **22**도 관리자의 IP에만 허용합니다.
- API **8000**, Qdrant **6333**, DB **3306/5432**는 외부에 열지 않습니다. API는 호스트 루프백에만 공개되고 화면은 Docker 내부 주소로 호출합니다.
- 서버에서 DNS 조회와 외부 HTTPS 연결이 가능해야 합니다. 런타임에는 OpenAI 및 Qdrant Cloud에, 빌드 시에는 컨테이너 레지스트리와 Python 패키지 저장소에 접근합니다. Qdrant 측 IP 제한을 사용한다면 EC2의 실제 송신 IP도 허용합니다.

이 설정은 `8501` 포트의 HTTP 접속을 제공합니다. 도메인으로 공개 운영할 때는 HTTPS 프록시/ALB를 앞에 두고 Streamlit의 WebSocket 전달을 설정하세요. 여러 화면 인스턴스로 확장할 때는 세션 고정도 필요합니다.

## 2. 환경변수

`.env`가 없다면 예제 파일을 복사합니다. 기존 `.env`가 있으면 덮어쓰지 마세요.

```bash
test -f .env || cp .env.example .env
chmod 600 .env
```

서버의 `.env`에 실제 값을 입력합니다. 키를 Git이나 Docker 이미지에 넣지 않습니다.

| 변수 | 설정 |
| --- | --- |
| `OPENAI_API_KEY` | 기존 OpenAI 키 |
| `OPENAI_BASE_URL` | 커스텀 엔드포인트를 쓸 때만 지정 |
| `OPENAI_MODEL_NAME` | 현재 사용하는 모델 |
| `GENERATION_MODEL_NAME` | 광고문 생성 모델 |
| `OPENAI_EMBEDDING_MODEL` | 기존 컬렉션을 만든 임베딩 모델과 동일하게 유지 |
| `QDRANT_URL` | 기존 Qdrant Cloud의 HTTPS 주소 |
| `QDRANT_API_KEY` | 기존 컬렉션 조회 권한이 있는 키 |
| `QDRANT_COLLECTION_NAME` | 기존 컬렉션 이름 |
| `JUDGE_BACKEND` | 현재 구현된 `rule` 또는 `gpt` |

Compose는 `.env`를 API 컨테이너에만 전달합니다. 화면에는 `API_BASE_URL=http://api:8000`과 `UI_DATA_MODE=api`를 직접 설정하므로 로컬 `.env`의 `localhost`나 `mock` 설정이 화면에 적용되지 않습니다. API의 프로젝트 루트와 BM25 경로도 컨테이너 내부 경로로 고정합니다.

## 3. 빌드와 실행

```bash
docker compose version
docker compose config --quiet
docker compose up -d --build --wait --wait-timeout 180
docker compose ps
```

`config --quiet`은 설정 내용을 출력하지 않고 문법을 검사합니다. 일반 `docker compose config` 출력에는 비밀키가 포함될 수 있으므로 공유하지 마세요.

- API와 화면은 Python 3.12 및 저장소의 `requirements.txt` 고정 버전을 사용합니다.
- 두 이미지에 규정 원문, 성분, 표현 은행, 창작 참고, 시장 비교, 매출 자료를 포함합니다.
- API 이미지 빌드 시 `chunks.jsonl`에서 **BM25만 생성**합니다. 로컬 PC의 pickle 파일은 복사하지 않습니다.
- 화면에는 `.streamlit/config.toml`, 폰트, 이미지 등 정적 파일을 포함합니다.
- 비밀키는 빌드에 필요하지 않으며, 빌드와 서버 시작은 Qdrant 컬렉션을 생성/변경하지 않습니다.
- API의 `/health`가 응답한 뒤 화면을 시작합니다. 컨테이너는 일반 사용자로 실행되며, 로그는 컨테이너당 10 MB × 3개로 순환합니다.

화면 주소: `http://<EC2_PUBLIC_IP>:8501`

`docker/`에서 `docker compose`를 실행하거나 `-f docker/docker-compose.yml`을 사용해도 루트 설정을 재사용합니다. 두 진입점은 동일한 Compose 프로젝트 이름을 사용합니다.

## 4. 배포 확인

```bash
# EC2 안에서 API / 화면 프로세스 상태 확인
curl --fail http://127.0.0.1:8000/health
curl --fail http://127.0.0.1:8501/_stcore/health

# 기존 Cloud 연결 및 컬렉션 존재·데이터 수 확인 (추론/임베딩 생성 없음)
docker compose exec api python scripts/check_connections.py

# 시작 실패 시 로그 확인
docker compose logs --tail=100 api app
```

컨테이너 헬스체크는 프로세스 응답만 확인합니다. Qdrant·OpenAI 연결이나 검색 품질까지 보장하지 않으므로 연결 점검을 별도로 수행합니다. 연결 점검은 OpenAI 모델 목록과 Qdrant 컬렉션 정보를 읽으며, 컬렉션을 수정하지 않습니다. `--inference`를 추가하면 유료 모델/임베딩 호출도 실행되므로 필요할 때만 사용하세요.

브라우저에서는 홈, 규정 열람, 성분/제품 입력, 시장 비교, 매출 시나리오를 확인하고 실제 문구 검토·생성을 한 번 실행합니다. 검토·생성에는 외부 API 사용 비용이 발생할 수 있습니다. `chunks.jsonl`과 Cloud 컬렉션은 같은 규정 데이터 버전이어야 합니다.

기존 컬렉션을 사용하는 최초 배포에는 `indexing/05_build_indexes.py` 전체 실행이 필요하지 않습니다. 전체 실행은 임베딩 생성과 Qdrant 쓰기를 포함하므로 규정 데이터를 갱신할 때 별도로 수행하세요.

## 5. 갱신과 중지

새 코드를 가져온 뒤 다시 빌드합니다. 실행 중인 세션의 제품·대화 정보는 재시작 시 사라질 수 있습니다.

```bash
docker compose up -d --build --wait --wait-timeout 180
docker compose exec api python scripts/check_connections.py
```

`.env`만 변경한 경우에도 `docker compose up -d --wait --wait-timeout 180`으로 설정을 반영합니다. `docker compose restart`만으로는 새 환경변수가 적용되지 않습니다.

```bash
docker compose down
```

컨테이너 중지는 외부 Qdrant Cloud 데이터에 영향을 주지 않습니다. `restart: unless-stopped`가 서버 재부팅 후 동작하려면 EC2에서 Docker 서비스도 자동 시작되도록 설정해야 합니다. 실행 중인 컨테이너가 `unhealthy`가 된 것만으로 자동 재시작되지는 않으므로 로그와 연결 상태를 확인하세요.

참고: [Docker Compose 시작 순서](https://docs.docker.com/compose/how-tos/startup-order/), [Compose include](https://docs.docker.com/reference/compose-file/include/), [Streamlit 배포 구조](https://docs.streamlit.io/develop/concepts/architecture/architecture).
