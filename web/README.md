# web — 뷰렛 Django 웹 서비스

3차 FastAPI AI 서버(저장소 루트 `api/`, `src/`)를 호출하는 Django 웹 서비스입니다.
Django는 회원·제품·이력(DB)과 화면을 맡고, 검토·생성·챗봇 판단은 모두 AI 서버에 맡깁니다.

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

테스트 (AI 서버 없이 mock 으로 동작):

```bash
uv run python manage.py test
```

## 앱 구성

| 앱 | 역할 | 주요 URL |
| --- | --- | --- |
| `core` | 홈, 헬스체크, **AI 서버 클라이언트(`core/ai_client.py`)** | `/`, `/health/` |
| `accounts` | 회원가입·로그인·로그아웃 (Django 기본 auth) | `/accounts/signup/`, `/accounts/login/`, `/accounts/logout/` (POST) |
| `products` | 내 제품 + 보유 실증 자료 CRUD | `/products/`, `/products/new/`, `/products/<id>/`, `/products/<id>/edit/`, `/products/<id>/delete/` |
| `reviews` | 문구 검토·광고문 생성과 이력 | `/reviews/new/`, `/reviews/<id>/`, `/reviews/`, `/reviews/generate/new/`, `/reviews/generate/<id>/`, `/reviews/generate/` |
| `chat` | 대화방·메시지 저장, 챗봇 | `/chat/`, `/chat/new/` (POST), `/chat/<id>/`, `/chat/<id>/send/` (POST, JSON) |

### 모델

- `Product` / `Evidence`: `Product.to_product_card()` 가 AI 서버의 `ProductCard` 형식으로 변환합니다.
- `ReviewRecord`, `GenerationRecord`: 요약 필드(판정·위반 유형 등) + AI 응답 원문(`response` JSON)을 저장합니다.
- `ChatSession` / `ChatMessage`: AI 서버가 돌려준 대화 맥락(`context`)을 세션에 저장해 다음 요청에 다시 보내고, 최근 12턴을 `history` 로 보냅니다.

## 프론트 작업 안내

- 템플릿: `web/templates/` (앱별 폴더), 공통 레이아웃 `base.html`, 조각 `partials/`
- 정적 파일: `web/static/css/base.css`, `web/static/js/chat.js`(챗봇), `web/static/js/loading.js`(제출 중 표시)
- 지금 화면은 동작 확인용 기본 디자인입니다. 템플릿 변수 이름만 유지하면 자유롭게 바꿔도 됩니다.
- 챗봇 전송 API: `POST /chat/<id>/send/`, 헤더 `X-CSRFToken`, 본문 `{"message": "..."}`
  → 성공 `{"user": {...}, "assistant": {"content", "intent", "response", ...}}`, 실패 `{"error": "..."}` (400/502)

## 배포 시 환경변수

EC2에서는 [Django/RDS 배포 가이드](../docker/README.django.md)와 루트 `docker-compose.web.yml`을 사용합니다. 운영용 예제는 `docker/web.env.example`이며, `DEBUG=False`일 때 MySQL 또는 PostgreSQL 연결과 50자 이상의 `DJANGO_SECRET_KEY`가 필수입니다. `/health/ready/`와 `manage.py check_database`로 DB 연결·마이그레이션 상태를 확인할 수 있습니다.

`web/.env.example` 참고. 운영에서는 최소한 다음을 설정합니다.

| 변수 | 예시 |
| --- | --- |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_SECRET_KEY` | 긴 임의 문자열 (필수) |
| `DJANGO_ALLOWED_HOSTS` | `13.125.x.x,beaurette.example.com` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `http://13.125.x.x` |
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
