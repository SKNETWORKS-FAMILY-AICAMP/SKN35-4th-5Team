# web — 뷰렛 4차 프로젝트 Django 웹 서비스

4차 프로젝트의 회원·제품·이력 관리를 제공하며, FastAPI AI 서버(저장소 루트 `api/`, `src/`)를 호출하는 Django 웹 서비스입니다.
Django는 회원·제품·이력(DB), 공통 화면, 규정 참고 자료 열람과 매출 시나리오 계산을 맡습니다. 검토·생성·챗봇·규정 검색은 FastAPI AI 서버를 호출합니다.

[배포 서비스](https://beaurette.duckdns.org) · [프로젝트 README](../README.md) · [AWS 배포 가이드](../docker/README.django.md)

```
브라우저 ──► Django (web/, :8001) ──httpx──► FastAPI AI 서버 (api/, :8000) ──► OpenAI · Qdrant
                 │
                 └──► DB (로컬 SQLite / 운영 MySQL 또는 PostgreSQL)
```

## 로컬 실행

```bash
# 1) AI 서버 (저장소 루트, 루트 .env 에 OPENAI/QDRANT 키 필요)
uv run uvicorn api.main:app --port 8000

# 2) Django (web/)
cd web
cp .env.example .env        # 필요한 값만 수정
uv sync
uv run python manage.py migrate
uv run python manage.py createsuperuser   # 관리자 페이지(/admin) 쓸 때만
uv run python manage.py runserver 8001
```

http://localhost:8001 접속. AI 서버 연결 상태는 http://localhost:8001/health/ 에서 확인합니다.

## 실행 상태 확인

`uv run python manage.py check`로 Django 설정을, `uv run python manage.py check_database`로 DB 연결과 마이그레이션 적용 상태를 확인합니다. `/health/ready/`는 DB 준비 상태를, `/health/`는 AI 서버 연결 상태를 반환합니다.

## 앱 구성

| 앱 | 역할 | 주요 URL |
| --- | --- | --- |
| `core` | 홈, 상세페이지 검토, 규정·가이드라인, 매출 시나리오, AI 클라이언트·준비 상태 점검 | `/`, `/bulk/`, `/library/`, `/forecast/`, `/health/`, `/health/ready/` |
| `accounts` | 회원가입·로그인·로그아웃 (Django 기본 auth) | `/accounts/signup/`, `/accounts/login/`, `/accounts/logout/` (POST) |
| `products` | 내 제품·실증 자료 CRUD, 23개 예시 제품 불러오기 | `/products/`, `/products/new/`, `/products/<id>/`, `/products/<id>/edit/`, `/products/<id>/delete/`, `/products/samples/<sample_id>/add/` (POST) |
| `reviews` | 문구 검토·광고문 생성과 이력 | `/reviews/new/`, `/reviews/<id>/`, `/reviews/`, `/reviews/generate/new/`, `/reviews/generate/<id>/`, `/reviews/generate/` |
| `chat` | 대화방·메시지 저장, 챗봇 | `/chat/`, `/chat/new/` (POST), `/chat/<id>/`, `/chat/<id>/send/` (POST, JSON) |

### 모델

- `Product` / `Evidence`: `Product.to_product_card()`가 AI 서버의 `ProductCard` 형식으로 변환합니다. `sample_id`·`source_note`는 예시 제품 출처를, `source_kind`·`source_url`은 보유 시험 보고서/공식몰 공개 요약을 구분합니다.
- `ReviewRecord`, `GenerationRecord`: 요약 필드(판정·위반 유형 등) + AI 응답 원문(`response` JSON)을 저장합니다.
- `ChatSession` / `ChatMessage`: AI 서버가 돌려준 대화 맥락(`context`)을 세션에 저장해 다음 요청에 다시 보내고, 최근 12개 메시지를 `history`로 보냅니다.

## 화면과 주요 동작

| 화면 | 구현 |
| --- | --- |
| 홈 | 비로그인 상태의 8개 섹션 랜딩, 로그인 상태의 내 제품·최근 검토 대시보드 |
| 공통 작업 공간 | 금빛·유리 질감의 공통 테마, Workspace / AI Lab / Insight / History 사이드바 |
| 제품 | 유형별 목록, 일반/기능성 필터, 예시 제품 복사, 시험 자료 출처 표시 |
| 검토·생성 | 제품 선택과 입력 폼, 결과·근거·후보 상태 표시, 이력 목록·상세 |
| 상세페이지 검토 | 최대 50,000자·100문장, 문장별 판정·수정 후보·근거·교정본 |
| 규정·가이드라인 | 검색(`tab=search`), 금지 표현 사전(`tab=banned`), 적발 사례(`tab=cases`) |
| 매출 시나리오 | 가격·판매량·위반 조건 입력, 결과 카드·차트·표와 원문/제안 문구 비교 |
| 챗봇 | 제품 선택, 대화방·맥락 유지, 비동기 메시지 전송 |

검토 결과는 검증을 통과한 수정 후보만 표시합니다. 제안이 없으면 안내와 탈락 사유를 보여줍니다. 생성 결과와 챗봇은 `제외` 후보를 숨기며 `확인필요` 후보에 경고를 표시합니다.

상세페이지 일괄 검토·규정 검색·예상 매출 시나리오는 요청 결과를 화면에 표시하며 별도 DB 이력 모델은 없습니다. 매출 시나리오는 입력 가정에 따른 계산이며 실제 광고 성과나 매출 상승을 보장하지 않습니다.

### 템플릿·정적 자산

- 랜딩: `templates/core/landing_jarvis.html`, `static/css/jarvis.css`, `static/js/jarvis.js`
- 공통 화면: `templates/base.html`, `static/css/base.css`, `static/css/app.css`, `static/js/app-shell.js`
- 제품 필터·매출 차트: `static/js/pd-filter.js`, `static/js/forecast-dash.js`
- 챗봇·처리 중 표시: `static/js/chat.js`, `static/js/loading.js`
- 폰트·브랜드·사진: `static/fonts/`, `static/brand/`, `static/landing/`

고정 참고 자료는 `core/reference/`에 포함됩니다. 규정·사례·처분 기준·효과 크기 자료가 바뀌면 해당 JSON과 원본 출처를 함께 갱신합니다. 예시 제품은 `products/sample_products.json`을 사용합니다.

### 챗봇 전송 API

`POST /chat/<id>/send/`, 헤더 `X-CSRFToken`, 본문 `{"message": "..."}`. 성공 시 `user`·`assistant` 메시지를, 실패 시 `{"error": "..."}`와 HTTP 400/502를 반환합니다. 사용자 메시지와 AI 응답은 성공 시 함께 저장합니다.

## 배포 시 환경변수

EC2에서는 [Django/RDS 배포 가이드](../docker/README.django.md)와 루트 `docker-compose.web.yml`을 사용합니다. 운영용 예제는 `docker/web.env.example`이며, `DEBUG=False`일 때 MySQL 또는 PostgreSQL 연결과 50자 이상의 `DJANGO_SECRET_KEY`가 필수입니다. `/health/ready/`와 `manage.py check_database`로 DB 연결·마이그레이션 상태를 확인할 수 있습니다.

`web/.env.example` 참고. 운영에서는 최소한 다음을 설정합니다.

| 변수 | 예시 |
| --- | --- |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_SECRET_KEY` | 긴 임의 문자열 (필수) |
| `DJANGO_ALLOWED_HOSTS` | `beaurette.duckdns.org,localhost,127.0.0.1` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://beaurette.duckdns.org` |
| `DATABASE_URL` | `mysql://beaurette_app:인코딩한비밀번호@RDS_엔드포인트:3306/beaurette` |
| `DATABASE_SSL_ROOT_CERT` | `/app/certs/rds-global-bundle.pem` (배포 이미지에 포함) |
| `AI_API_URL` | `http://api:8000` (docker-compose 서비스 이름) |

실행 명령 (컨테이너):

```bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput   # Docker 빌드에서 실행, Caddy가 /static/ 으로 서빙
gunicorn config.wsgi:application --bind 0.0.0.0:8001 --workers 2 --timeout 200
```

AI 응답이 1~2분 걸릴 수 있으므로 배포 설정은 Gunicorn timeout 200초, Caddy response_header_timeout 210초를 사용합니다. DB 마이그레이션은 서버 시작 전에 별도 명령으로 실행합니다.
