# Beaurette | 뷰렛

**화장품 광고 문구를 규정 근거로 검토하고, 회원별 제품·실증 자료와 검토·생성·대화 이력을 관리하는 AI 웹 서비스**

SK Networks Family AI Camp 35기 · **4차 프로젝트 · 5팀**

기존 RAG 에이전트를 FastAPI AI 서버로 활용하고, Django 웹 서비스와 AWS EC2 · RDS 배포 구성을 더했습니다.

[팀 저장소](https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN35-4th-5Team) · [Django 웹 가이드](web/README.md) · [AI API 가이드](api/README.md) · [AWS 배포 가이드](docker/README.django.md) · [4차 역할 분담 계획서](plan.md)

<h2 align="center">🛠️ Tech Stack</h2>

<table align="center">
  <thead>
    <tr><th align="center">Category</th><th align="center">Technologies</th></tr>
  </thead>
  <tbody>
    <tr><td align="center"><strong>Languages</strong></td><td align="center"><img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=flat&amp;logo=python&amp;logoColor=white"> <img alt="JavaScript" src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&amp;logo=javascript&amp;logoColor=black"> <img alt="CSS" src="https://img.shields.io/badge/CSS-663399?style=flat&amp;logo=css&amp;logoColor=white"></td></tr>
    <tr><td align="center"><strong>Backend &amp; UI</strong></td><td align="center"><img alt="Django" src="https://img.shields.io/badge/Django-092E20?style=flat&amp;logo=django&amp;logoColor=white"> <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688?style=flat&amp;logo=fastapi&amp;logoColor=white"> <img alt="Pydantic" src="https://img.shields.io/badge/Pydantic-E92063?style=flat&amp;logo=pydantic&amp;logoColor=white"> <img alt="HTML5" src="https://img.shields.io/badge/HTML5-E34F26?style=flat&amp;logo=html5&amp;logoColor=white"></td></tr>
    <tr><td align="center"><strong>AI &amp; Agents</strong></td><td align="center"><img alt="OpenAI API" src="https://img.shields.io/badge/OpenAI_API-412991?style=flat"> <img alt="LangChain" src="https://img.shields.io/badge/LangChain-1C3C3C?style=flat&amp;logo=langchain&amp;logoColor=white"> <img alt="LangGraph" src="https://img.shields.io/badge/LangGraph-1C3C3C?style=flat&amp;logo=langgraph&amp;logoColor=white"></td></tr>
    <tr><td align="center"><strong>Database &amp; Search</strong></td><td align="center"><img alt="MySQL" src="https://img.shields.io/badge/MySQL-4479A1?style=flat&amp;logo=mysql&amp;logoColor=white"> <img alt="SQLite" src="https://img.shields.io/badge/SQLite-003B57?style=flat&amp;logo=sqlite&amp;logoColor=white"> <img alt="Qdrant Cloud" src="https://img.shields.io/badge/Qdrant_Cloud-DC244C?style=flat&amp;logo=qdrant&amp;logoColor=white"> <img alt="BM25" src="https://img.shields.io/badge/BM25-2563EB?style=flat"> <img alt="Hybrid RRF" src="https://img.shields.io/badge/Hybrid_RRF-7C3AED?style=flat"></td></tr>
    <tr><td align="center"><strong>Server &amp; Cloud</strong></td><td align="center"><img alt="AWS EC2" src="https://img.shields.io/badge/AWS_EC2-FF9900?style=flat"> <img alt="Amazon RDS" src="https://img.shields.io/badge/Amazon_RDS-527FFF?style=flat"> <img alt="Docker Compose" src="https://img.shields.io/badge/Docker_Compose-2496ED?style=flat&amp;logo=docker&amp;logoColor=white"> <img alt="Caddy" src="https://img.shields.io/badge/Caddy-1F88C0?style=flat"> <img alt="Gunicorn" src="https://img.shields.io/badge/Gunicorn-499848?style=flat&amp;logo=gunicorn&amp;logoColor=white"> <img alt="Uvicorn" src="https://img.shields.io/badge/Uvicorn-4051B5?style=flat"></td></tr>
    <tr><td align="center"><strong>Tools &amp; Testing</strong></td><td align="center"><img alt="uv" src="https://img.shields.io/badge/uv-DE5FE9?style=flat&amp;logo=uv&amp;logoColor=white"> <img alt="Git" src="https://img.shields.io/badge/Git-F05032?style=flat&amp;logo=git&amp;logoColor=white"> <img alt="GitHub" src="https://img.shields.io/badge/GitHub-181717?style=flat&amp;logo=github&amp;logoColor=white"> <img alt="pytest" src="https://img.shields.io/badge/pytest-0A9EDC?style=flat&amp;logo=pytest&amp;logoColor=white"></td></tr>
  </tbody>
</table>

## 팀원 소개

<table align="center">
  <tbody>
    <tr>
      <td align="center" valign="middle" width="160"><img src="docs/team/kim-gyeongmin-portrait.jpg" alt="김경민 소개 이미지" width="160" height="213"></td>
      <td align="center" valign="middle" width="160"><img src="docs/team/kwon-junho-portrait.jpg" alt="권준호 소개 이미지" width="160" height="213"></td>
      <td align="center" valign="middle" width="160"><img src="docs/team/lee-hyeongmin-portrait.jpg" alt="이형민 소개 이미지" width="160" height="213"></td>
      <td align="center" valign="middle" width="160"><img src="docs/team/lee-sehee-portrait.jpg" alt="이세희 소개 이미지" width="160" height="213"></td>
    </tr>
    <tr>
      <td align="center"><strong>김경민</strong></td>
      <td align="center"><strong>권준호</strong></td>
      <td align="center"><strong>이형민</strong></td>
      <td align="center"><strong>이세희</strong></td>
    </tr>
  </tbody>
</table>

<p align="center"><sub>위 인물 이미지는 AI를 활용해 생성·편집한 팀원 소개용 이미지입니다.</sub></p>

### 4차 프로젝트 역할 및 기여

| 팀원 | 작업 브랜치 | 담당 영역 | 관련 코드 및 반영 내역 |
| --- | --- | --- | --- |
| **김경민** | [`kgm`](https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN35-4th-5Team/tree/kgm) | AWS EC2 · RDS 배포, Docker Compose, Caddy · Gunicorn 운영 구성 | [`docker/`](docker/) · [`docker-compose.web.yml`](docker-compose.web.yml) · [Django/RDS 배포 구성](https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN35-4th-5Team/commit/5035137) |
| **권준호** | [`kjh`](https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN35-4th-5Team/tree/kjh) | Django 템플릿 · CSS · JavaScript, 기존 브랜드 디자인의 웹 화면 이식 | 담당 경로: [`web/templates/`](web/templates/) · [`web/static/`](web/static/) |
| **이형민** | [`lhm`](https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN35-4th-5Team/tree/lhm) | Django 백엔드, 회원·제품·실증·이력 모델, AI 서버 연동, 브랜치 통합 | [`web/`](web/) · [Django 웹 서비스 구현](https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN35-4th-5Team/commit/4eb4d4a) · [환경변수 처리 보완](https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN35-4th-5Team/commit/814fd0a) |
| **이세희** | [`lsh`](https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN35-4th-5Team/tree/lsh) |  |  |

담당 영역은 [4차 역할 분담 계획서](plan.md), 반영 내역은 현재 저장소의 구현 커밋을 기준으로 정리했습니다. 담당 경로는 작업 범위를 나타내며, 해당 경로의 모든 코드를 개인 단독 기여로 의미하지 않습니다.

---

<details>
<summary>기존 Streamlit 기능 참고 화면 (2026-10-15)</summary>

아래 이미지는 기존 Streamlit 앱의 기능 참고 자료입니다. 4차 Django 웹 화면과는 다르며, 현재 웹 서비스의 실행 방법과 화면 구성은 [Django 웹 가이드](web/README.md)를 참고하세요. 이미지를 누르면 원본 크기로 볼 수 있습니다.

[![기존 Streamlit 홈 화면](docs/screenshots/home-2026-10-15.jpg)](docs/screenshots/home-2026-10-15.jpg)

| 문구 검토 · 규정 근거 | 수정 후보 · 역검증 |
| :---: | :---: |
| [![실제 API 검토 결과와 근거 조항](docs/screenshots/review-2026-10-15.jpg)](docs/screenshots/review-2026-10-15.jpg) | [![표현 강도별 수정 후보와 역검증 결과](docs/screenshots/review-candidates-2026-10-15.jpg)](docs/screenshots/review-candidates-2026-10-15.jpg) |
| 문제 표현과 연결된 규정 원문 확인 | 근거 최대·균형·가장 안전 후보 선택 |

| 통합 챗봇 | 광고문 생성 |
| :---: | :---: |
| [![기존 통합 챗봇과 제품 검토 기준](docs/screenshots/chat-2026-10-15.jpg)](docs/screenshots/chat-2026-10-15.jpg) | [![실제 생성 후보와 매출 시나리오 연결 버튼](docs/screenshots/generate-2026-10-15.jpg)](docs/screenshots/generate-2026-10-15.jpg) |
| 화장품·성분 Q&A부터 생성·검토까지 | 검토를 통과한 후보 확인 및 매출 시나리오 연결 |

| 내 제품 · 시장 비교 | 예상 매출 시나리오 |
| :---: | :---: |
| [![제품 실증 자료와 유사 시장 제품 비교](docs/screenshots/market-2026-10-15.jpg)](docs/screenshots/market-2026-10-15.jpg) | [![가정에 따른 매출 상승·하락 시나리오](docs/screenshots/forecast-2026-10-15.jpg)](docs/screenshots/forecast-2026-10-15.jpg) |
| 예시 제품의 성분·기능성·제형을 기준으로 비교 | 입력 가정에 따른 변화 범위 확인 |

검토·광고문 생성 이미지는 실제 API 실행 결과입니다. 시장 비교·매출 화면은 앱에서 제공하는 비타민A 앰플 예시를 사용했으며, 표시된 판매량과 매출 변화는 가정 기반 시나리오입니다.

</details>

## 1. 프로젝트 소개

화장품 광고는 같은 표현이라도 일반/기능성 제품 여부와 보유 시험 자료에 따라 검토 결과가 달라집니다. 규정 문서를 찾는 일과 실제로 사용할 수 있는 대체 문구를 만드는 일이 분리되어 있어, 마케터가 작성과 검토를 반복해야 합니다.

뷰렛은 **회원가입 → 내 제품·실증 자료 등록 → 문구 검토·광고문 생성 → 근거·수정 제안 확인 → 이력 조회**를 하나의 웹 서비스로 연결합니다. FastAPI와 LangGraph 기반 AI 엔진이 규정 검색·판정·교정·재검증을 수행하고, Django가 회원별 데이터와 화면을 관리합니다.

4차 프로젝트는 **LLM을 연동한 문서 기반 질의응답 웹 서비스 개발 및 배포**에 초점을 둡니다. 현재 저장소에는 Django 웹 앱과 AWS EC2용 Docker Compose 구성이 포함되어 있으며, 운영 DB는 RDS MySQL, 웹 진입점은 Caddy · Gunicorn을 사용하도록 구성했습니다. 로컬 개발은 SQLite를 사용합니다.

| 해결하려는 문제 | 구현 방식 |
| --- | --- |
| 판정 이유와 출처를 확인하기 어려움 | 법령·고시·지침·사례를 검색하고 조항 번호와 원문 스니펫 제공 |
| 같은 문구를 제품 맥락 없이 일괄 판정 | 제품 분류·기능성 유형·보유 실증 자료를 판정과 생성에 반영 |
| LLM이 수정하면서 위험 표현이나 숫자를 다시 생성 | 생성 결과를 규칙 엔진·실증 수치 검증기로 재검사 |
| 안전한 표현만 남기면서 광고의 구체성이 사라짐 | 제형·사용감·성분 역할·확인된 제품 사실을 생성 재료로 활용 |
| 제품·검토 결과를 계정별로 보관하고 다시 확인하기 어려움 | Django 인증과 DB 모델로 제품·실증·검토·생성·대화 이력 저장 |
| 웹 서비스와 AI 서버를 함께 운영해야 함 | Caddy → Django → FastAPI 구조와 Docker Compose, DB 준비 상태 점검 구성 |

이 서비스는 광고 사전 검토를 돕는 프로토타입입니다. 결과는 수집된 규정과 구현된 규칙에 기반한 검토 의견이며, 최종 법률 판단이나 광고 적합성 인증을 대신하지 않습니다.

## 2. 주요 기능

| 기능 | 제공 내용 |
| --- | --- |
| **회원가입·로그인** | Django 기본 인증, 로그인 사용자별 제품·검토·생성·대화 접근 제한 |
| **내 제품·실증 자료 관리** | 제품과 보유 실증 자료 등록·조회·수정·삭제, AI 서버의 ProductCard 형식으로 변환 |
| **단일 문구 검토** | 가능·조건부·불가 판정, 문제 표현, 근거 조항, 추가로 필요한 시험 안내 |
| **교정 후보 제안** | 제품의 실증 범위에 따른 수정 제안과 AI 서버의 재검증 결과 확인 |
| **광고문 생성** | 작성 요청·채널·어조·제품 정보를 반영하고, 규정 검색·후보 검증·필요 시 재작성 |
| **검토·생성 이력** | 사용자별 입력과 AI 응답 저장, 목록·상세 조회, 제품별 검토 이력 필터링 |
| **통합 챗봇** | 대화방·메시지·맥락 저장, 최근 12개 메시지 전달, 검토·생성·화장품/성분 Q&A 분기 |
| **운영 상태 점검** | AI 연결 상태와 DB 연결·미적용 마이그레이션 점검 경로 제공 |

상세페이지 일괄 검토와 규정 검색은 AI API에 남아 있습니다. 시장 비교·매출 시나리오 등 기존 Streamlit 화면의 기능은 [기존 UI 가이드](app/README.md)에 정리되어 있으며, 현재 Django 웹 화면에는 별도로 연결되어 있지 않습니다.

### 사용 흐름

1. **회원가입·로그인**: 내 계정으로 웹 서비스에 접속합니다.
2. **내 제품 등록**: 일반/기능성 여부와 성분·제품 사실·보유 실증을 입력합니다.
3. **검토 또는 생성**: 제품을 선택하고 기존 광고 문구나 채널·어조를 포함한 작성 요청을 입력합니다.
4. **결과 확인**: 판정, 근거 조항, 수정 제안 또는 생성 후보를 확인합니다.
5. **이력 조회·대화 이어가기**: 저장된 결과를 다시 열거나 제품과 연결된 챗봇 대화를 이어갑니다.

예를 들어 동일한 수치 광고라도 해당 효능·기간·수치를 뒷받침하는 보유 시험이 있는지에 따라 결과와 교정 방향이 달라집니다. 성분의 일반적인 역할 설명은 특정 완제품의 효능 시험으로 취급하지 않습니다.

## 3. 시스템 아키텍처

Django는 인증·화면·DB 저장을 맡고, FastAPI는 규정 검색과 AI 워크플로를 수행합니다. 운영 구성의 `proxy`, `web`, `api`는 EC2에서 실행하며 RDS와 Qdrant Cloud에 연결합니다.

```mermaid
flowchart LR
    U[사용자 브라우저] --> PROXY[Caddy · HTTPS / 정적 파일]
    subgraph EC2[AWS EC2 · Docker Compose]
        PROXY --> WEB[Gunicorn + Django]
        WEB --> API[FastAPI · Uvicorn]
    end
    WEB --> DB[(Amazon RDS · MySQL)]
    API --> CHAT[자연어 의도·대화 맥락 처리]
    API --> REVIEW[LangGraph 검토 워크플로]
    API --> GEN[LangGraph 생성 워크플로]
    CHAT --> REVIEW
    CHAT --> GEN
    CHAT --> RAG[Hybrid Retriever]
    REVIEW --> RAG
    GEN --> RAG
    RAG --> Q[Qdrant Cloud · Dense]
    RAG --> B[BM25 · Sparse]
    REVIEW --> LLM[OpenAI]
    GEN --> LLM
    CHAT --> LLM
    REVIEW --> V[규칙·실증 수치 역검증]
    GEN --> V
    RAW[법령·고시·지침·사례] --> CHUNK[조항 청킹·메타데이터 보강]
    CHUNK --> Q
    CHUNK --> B
```

로컬에서는 Django 개발 서버와 SQLite를 사용합니다. 배포 시에는 `docker-compose.web.yml`이 Caddy · Django · FastAPI를 실행하고, 기존 RDS와 Qdrant Cloud에 연결합니다. RDS 및 Qdrant 서버를 Compose에서 새로 만들지는 않습니다.

### 검토 워크플로

![Beaurette 검토 워크플로 · 주요 처리와 예외 경로](docs/diagrams/review-workflow-animated.svg)

<details>
<summary>상세 분기 보기 (Mermaid)</summary>

```mermaid
flowchart TD
    A[입력 정규화] --> B[규칙 검사]
    B --> C[사전 판정]
    C --> D[검색 질의 작성]
    D --> E[하이브리드 검색]
    E --> F{근거 충분성}
    F -->|재검색 가능| D
    F -->|재시도 소진| J[최종 결과·판단보류]
    F -->|충분| G[근거 정리·판정 분기]
    G -->|교정 불필요| J
    G -->|교정 필요| H[실증 범위 내 후보 제안]
    H --> I{역검증}
    I -->|실패·재시도 가능| H
    I -->|검증 결과 확정| J
```

</details>

검토 그래프는 9개 노드로 구성하고 재검색·재제안 횟수를 제한합니다. 생성 그래프는 별도로 구성하되 같은 규칙 엔진과 검증기를 재사용합니다. 조건부·불가 판정에는 근거 조항을, 조건부 판정에는 필요한 추가 시험을 포함하도록 Pydantic 응답 계약을 검증합니다.

## 4. 핵심 구현과 기술적 의사결정

### 웹 서비스와 AI 서버 분리

Django는 [`core/ai_client.py`](web/core/ai_client.py)를 통해 FastAPI를 호출합니다. 제품·실증 모델을 AI 요청 형식으로 변환하고, 정상 응답은 검토·생성 이력에 저장합니다. 연결 실패·시간 초과·API 오류는 사용자 메시지로 처리하며 실패 요청은 이력으로 저장하지 않습니다.

제품·검토·생성·대화 조회는 로그인 사용자 기준으로 제한합니다. 챗봇은 메시지와 AI 응답의 맥락을 DB에 저장해 다음 요청에 활용합니다.

구현: [`products/`](web/products/) · [`reviews/`](web/reviews/) · [`chat/`](web/chat/)

### 영속 저장과 배포 준비 상태 확인

개발 환경은 SQLite, 운영 구성은 RDS MySQL을 사용하며 PostgreSQL도 지원합니다. 운영 설정에서는 DB 연결 정보와 50자 이상의 비밀키가 필요하고, RDS 연결 시 인증서와 호스트명을 검증합니다. 스키마 변경은 배포 과정에서 명시적으로 적용하며 `/health/ready/`가 DB 연결과 미적용 마이그레이션을 확인합니다.

Caddy가 HTTPS와 정적 파일을 제공하고 Gunicorn은 Docker 내부에서 Django를 실행합니다. 구성과 실행 순서는 [Django/RDS 배포 가이드](docker/README.django.md)를 따릅니다.

### 하이브리드 검색과 출처 보존

- 원문을 조항 단위로 나누고 출처·조항·법적 효력·제품 범위를 메타데이터로 보존합니다.
- OpenAI 임베딩 기반 Dense 검색과 BM25 검색을 가중 RRF로 결합합니다.
- 검색용 설명·키워드를 색인에 보강하되, 사용자에게 인용하는 문장은 규정 원문을 사용합니다.
- 검토 검색은 기본 Top 4를 사용하고 경량 reranker로 내부 순서를 조정합니다. 생성 흐름은 별도 검색 개수를 사용합니다.
- Dense 검색에 실패하면 BM25로 검색을 이어가며, 근거가 부족하면 판단보류 경로를 사용합니다.

구현: [`rag/`](src/cosmetic_agent/rag/) · [`indexing/`](indexing/) · [검색 설정](configs/retrieval.yaml)

### 규칙 판정을 하한으로 두는 구조

규칙·GPT zero-shot·few-shot을 동일 개발셋에서 비교한 결과, GPT의 정상 문구 과잉 경고와 불가→조건부 완화가 확인됐습니다. 기본 판정 백엔드는 `rule`로 두고, GPT를 사용하는 경우에도 명확한 규칙 위반과 실증 수치 충돌을 더 낮은 위험도로 덮어쓰지 않도록 구성했습니다.

구현: [`rules.py`](src/cosmetic_agent/domain/rules.py) · [`gpt_judge.py`](src/cosmetic_agent/models/gpt_judge.py) · [판정 평가 보고서](eval/reports/dev_comparison_2026-10-13.md)

### 실증 수치의 잘못된 조합 차단

모든 시험의 숫자를 합쳐 비교하면 서로 다른 시험의 기간·수치를 조합한 문구가 통과할 수 있습니다. 이를 막기 위해 한 문장의 수치와 기간이 **같은 효능의 단일 시험 기록**에 함께 존재하는지 확인합니다. 시험기관 이름의 숫자는 효능 결과로 인정하지 않습니다.

예: 보습 시험의 `4주·35%`와 탄력 시험의 `2주·70%`를 이용해 `2주 보습력 70% 개선`을 만드는 경우를 차단합니다.

구현: [`verifier.py`](src/cosmetic_agent/domain/verifier.py) · [회귀 테스트](tests/unit/test_review_regressions.py)

### 생성과 검증의 분리

LLM은 확인된 제품 사실·성분 역할·시장 표현을 재료로 후보를 작성하고, 코드가 금지 표현·기능성 범위·실증 수치를 다시 검사합니다. 검증 실패 사유는 재작성 입력에 반영합니다. 후보 선별에는 표현 매력도 평가도 활용하지만, 매출 상승이나 실제 광고 성과를 보장하는 점수로 해석하지 않습니다.

구현: [`generation/`](src/cosmetic_agent/generation/) · [`copy_suggester.py`](src/cosmetic_agent/models/copy_suggester.py) · [`appeal_ranker.py`](src/cosmetic_agent/models/appeal_ranker.py)

## 5. 데이터와 평가

아래 데이터와 수치는 기존 AI 엔진에서 이어받은 평가 자료입니다. 각 보고서의 측정 시점을 유지했으며, 4차 Django 웹 서비스와 AWS 배포의 통합 테스트 결과는 포함하지 않습니다. 웹 서비스 검증 방법은 [테스트와 평가 재현](#8-테스트와-평가-재현)에 정리했습니다.

### 데이터 구성

| 구분 | 내용 | 상세 문서 |
| --- | --- | --- |
| 규정 원문 | 화장품법·시행규칙·고시·관리지침·부당광고 적발 사례 | [원본 데이터](data/01_raw/README.md) |
| 검색 데이터 | 조항 청크·검색 메타데이터, Qdrant 및 BM25 인덱스 | [`data/02_processed/`](data/02_processed/) |
| 규칙 자산 | 금지 표현·기능성 범위·표현 단계·제품 예시 | [`data/assets/`](data/assets/) |
| 판정 벤치마크 | 팀 작성 dev 45문항·holdout 21문항 | [`data/golden_set/`](data/golden_set/) |
| 성분 지식 | 원료성분 사전 및 생성·설명용 성분 참고 자료 | [성분 지식](data/ingredient_knowledge/README.md) |
| 시장·표현 참고 | 시장 제품·광고 문구·표현 은행 | [시장 자료](data/market_reference/README.md) · [표현 은행](data/copy_bank/README.md) |
| 시나리오 참고 | 공개 비교 실험·처분 기준·문구 효과 크기 자료 | [매출 시나리오 자료](data/sales_forecast_reference/README.md) |

원본 문서의 버전·수집 내역·출처는 각 데이터 문서에 기록합니다. 규칙 자산을 변경할 때는 [`scripts/build_rule_assets.py`](scripts/build_rule_assets.py)를 수정한 뒤 다시 생성합니다.

### 판정 백엔드 비교

2026-10-13 저장 보고서 기준, 팀 작성 **dev 45문항**에 대한 독립 사전 판정 결과입니다. 검색·교정·역검증을 포함한 전체 서비스 평가는 아닙니다.

| 지표 | Rule | GPT zero-shot | GPT few-shot |
| --- | ---: | ---: | ---: |
| 수준 정확도 | 100.0% (45/45) | 68.9% (31/45) | 73.3% (33/45) |
| Macro-F1 (0/1/2 고정) | 1.000 | 0.639 | 0.612 |
| 불가→가능 오류 | 0건 | 0건 | 0건 |
| 불가→조건부 오류 | 0건 | 6건 | 1건 |
| 정상 문구 과잉 경고 | 0.0% | 50.0% | 66.7% |

규칙 개발에 사용한 소규모 개발셋이므로 Rule의 100%를 미관측 문구에 대한 성능으로 일반화할 수 없습니다. few-shot은 전체 정확도를 높였지만 정상 문구 과잉 경고도 늘려 Macro-F1은 낮아졌습니다.

출처: [판정 비교 보고서 및 오류 분석](eval/reports/dev_comparison_2026-10-13.md)

### 검색 방식 비교

2026-10-14 저장 보고서 기준입니다. 검색 인덱스는 59개 청크이며, 필수 인용 정답이 있는 dev 33문항·holdout 16문항만 검색 지표에 포함했습니다.

| 평가셋 | 검색 방식 | Strict Hit@4 | Evidence Coverage@4 | MRR |
| --- | --- | ---: | ---: | ---: |
| dev (33) | Dense | 42.4% | 66.7% | 0.3351 |
| dev (33) | BM25 | 57.6% | 81.8% | 0.4904 |
| dev (33) | **Hybrid** | **69.7%** | **81.8%** | **0.5404** |
| holdout 회귀셋 (16) | Dense | 43.8% | 56.2% | 0.4376 |
| holdout 회귀셋 (16) | BM25 | 50.0% | 93.8% | 0.4062 |
| holdout 회귀셋 (16) | **Hybrid** | **75.0%** | **100.0%** | **0.4369** |

- **Strict Hit@4**: 지정된 필수 근거가 상위 4개 결과에 포함된 비율입니다.
- **Evidence Coverage@4**: 필수 근거 또는 평가셋이 허용한 관련 근거가 포함된 비율입니다. 최종 답변의 법적 정확도나 충분성을 뜻하지 않습니다.
- **MRR**: 첫 필수 근거의 순위 역수 평균입니다.

holdout은 반복 실행하는 고정 회귀셋으로 사용했으므로 블라인드 최종 성능으로 제시하지 않습니다. 표는 해당 날짜에 저장된 결과이며 이후 코드 변경의 성능을 보증하지 않습니다.

출처: [dev 검색 보고서](eval/reports/rag_retrieval_dev_2026-10-14.md) · [holdout 검색 보고서](eval/reports/rag_retrieval_holdout_2026-10-14.md)

## 6. 로컬 실행

Python 3.11 이상과 `uv`가 필요합니다. AI 서버는 저장소 루트, Django 웹은 `web/`의 별도 Python 프로젝트로 실행합니다. 실제 검토·생성에는 OpenAI API 키와 Qdrant Cloud 접속 정보가 필요하며 API 사용 비용이 발생할 수 있습니다.

### 저장소와 AI 서버 환경 준비

```powershell
git clone https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN35-4th-5Team.git
cd SKN35-4th-5Team
uv sync --extra dev
Copy-Item .env.example .env
```

루트 `.env`에 다음 값을 설정합니다. 기존 `.env`가 있으면 복사 단계는 건너뜁니다. 발급받은 키는 로컬 환경 또는 배포 서버의 환경변수로 관리합니다.

```dotenv
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL_NAME=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

QDRANT_URL=https://your-cluster.region.cloud.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=cosmetic_ad_rules_v2
BM25_INDEX_PATH=data/02_processed/bm25_index.pkl

JUDGE_BACKEND=rule
```

### Django 환경 준비

저장소 루트에서 실행합니다. `web/.env`가 이미 있으면 복사 단계는 건너뜁니다.

```powershell
Copy-Item web/.env.example web/.env
cd web
uv sync
uv run python manage.py migrate
cd ..
```

로컬 개발용 `web/.env`의 주요 설정은 다음과 같습니다. `DJANGO_DEBUG=True`에서 `DATABASE_URL`을 비워두면 `web/db.sqlite3`에 회원·제품·이력을 저장합니다.

```dotenv
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=
AI_API_URL=http://localhost:8000
AI_API_TIMEOUT=180
```

### 검색 인덱스 준비

자신의 Qdrant 컬렉션을 처음 구성하거나 원문을 갱신한 경우 실행합니다. 05 단계에서 임베딩 생성과 Qdrant 쓰기가 발생합니다.

```powershell
uv run python indexing/03_chunk_articles.py
uv run python indexing/04_enrich_metadata.py
uv run python indexing/05_build_indexes.py
```

05 단계는 컬렉션이 없으면 생성하고 청크 ID 기반으로 upsert하며 로컬 BM25 파일도 만듭니다. 같은 청크를 재실행할 수 있지만, 원문에서 제거된 청크의 기존 벡터까지 자동 삭제하는 절차는 아닙니다. BM25 파일은 실행 환경에 포함하거나 배포 시 생성해야 합니다.

### AI 서버와 Django 웹 실행

서로 다른 터미널을 저장소 루트에서 열어 실행합니다.

```powershell
# 터미널 1: API
uv run uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

```powershell
# 터미널 2: Django 웹
cd web
uv run python manage.py runserver 8001
```

- 웹 화면: [http://localhost:8001](http://localhost:8001)
- AI 연결 상태: [http://localhost:8001/health/](http://localhost:8001/health/)
- DB 준비 상태: [http://localhost:8001/health/ready/](http://localhost:8001/health/ready/)
- Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)

회원가입 후 제품을 등록하고 문구 검토·광고문 생성·챗봇을 사용할 수 있습니다. 관리자 화면이 필요하면 `web/`에서 `uv run python manage.py createsuperuser`를 실행합니다. 실행 환경에 이미 설정한 환경변수는 `.env`보다 우선합니다.

### Docker / AWS EC2 실행

4차 웹 서비스는 **`docker-compose.web.yml`**로 배포합니다. EC2에서 Caddy · Django · FastAPI를 실행하고, 회원·제품·검토·생성·대화 데이터는 RDS MySQL에 저장하도록 구성했습니다. Caddy가 정적 파일과 도메인 HTTPS를 제공합니다.

먼저 [Django/RDS 배포 가이드](docker/README.django.md)에 따라 RDS DB와 네트워크를 준비하고, AI 서버용 루트 `.env`와 Django용 `web/.env`를 설정합니다. 운영용 예제는 [`docker/web.env.example`](docker/web.env.example)입니다.

설정 후 저장소 루트에서 빌드·연결 점검·마이그레이션·실행 순서로 진행합니다.

```bash
docker compose --env-file web/.env -f docker-compose.web.yml config --quiet
docker compose --env-file web/.env -f docker-compose.web.yml build api web proxy
docker compose --env-file web/.env -f docker-compose.web.yml run --rm --no-deps web python manage.py check_database --allow-unmigrated
docker compose --env-file web/.env -f docker-compose.web.yml run --rm --no-deps web python manage.py migrate --plan
docker compose --env-file web/.env -f docker-compose.web.yml run --rm --no-deps web python manage.py migrate --noinput
docker compose --env-file web/.env -f docker-compose.web.yml run --rm --no-deps web python manage.py check_database
docker compose --env-file web/.env -f docker-compose.web.yml up -d --wait --wait-timeout 180
docker compose --env-file web/.env -f docker-compose.web.yml ps
```

초기 설정은 서버 루프백에서 HTTP로 확인하고, 공개 시에는 실제 도메인·HTTPS 설정을 적용합니다. SSH 터널, 보안 그룹, DNS, 인증서 및 갱신 절차는 배포 가이드를 참고하세요. `/health/ready/`는 DB 준비 상태를 검사하고, `/health/`는 AI 연결 상태를 응답 본문으로 보고합니다.

<details>
<summary>기존 Streamlit 앱 실행 (참고용)</summary>

AI 서버가 실행 중일 때 저장소 루트에서 실행합니다.

```powershell
$env:UI_DATA_MODE = "api"
$env:API_BASE_URL = "http://localhost:8000"
uv run streamlit run app/streamlit_app.py
```

화면은 [http://localhost:8501](http://localhost:8501)에서 확인합니다. `UI_DATA_MODE=mock`은 화면 확인용 예시 모드입니다. 기존 `docker-compose.yml`은 FastAPI와 Streamlit을 실행하며, [Streamlit 배포 가이드](docker/README.md)와 [UI 가이드](app/README.md)에 설명되어 있습니다.

</details>

## 7. API

### Django 웹 경로

브라우저는 Django를 통해 제품·검토·생성·대화 데이터를 사용합니다. 기능 페이지는 로그인 후 접근하며, AI 요청은 Django 서버가 FastAPI로 전달합니다.

| 경로 | 기능 |
| --- | --- |
| `/accounts/signup/`, `/accounts/login/`, `/accounts/logout/` | 회원가입·로그인·로그아웃 |
| `/products/` | 내 제품과 실증 자료 관리 |
| `/reviews/new/`, `/reviews/` | 문구 검토 요청·이력 조회 |
| `/reviews/generate/new/`, `/reviews/generate/` | 광고문 생성 요청·이력 조회 |
| `/chat/` | 대화방 목록과 챗봇 |
| `/health/` | AI 서버 연결 상태 진단 |
| `/health/ready/` | DB 연결·마이그레이션 준비 상태, 실패 시 HTTP 503 |

### FastAPI AI 엔드포인트

| Method | 경로 | 기능 |
| --- | --- | --- |
| GET | `/health` | 서버 생존 확인; 모델·검색기 가용성 검사는 별도 |
| POST | `/review` | 단일 광고 문구 검토 |
| POST | `/review/bulk` | 상세페이지 문장별 일괄 검토 |
| POST | `/generate` | 신규 광고문 생성 및 검증 |
| POST | `/chat` | 자연어 요청 해석과 대화형 검토·생성·질문 답변 |
| GET | `/search` | 규정 하이브리드 검색 |

`POST /review` 요청 예시:

```json
{
  "copy_text": "매일 촉촉하게 가꾸는 피부",
  "product": {
    "product_id": "DEMO_CREAM_001",
    "name": "데모 수분 크림",
    "category": "일반",
    "functional_type": null,
    "owned_evidence": []
  }
}
```

응답은 `request_id`, `input_text`, `result`, `timing`을 포함합니다. `result.level`은 0(가능)·1(조건부)·2(불가)이며 판단보류 시 `null`입니다. 근거는 `citations`, 교정 문구는 `suggestion`, 필요한 추가 시험은 `next_test`로 제공합니다. 상세 계약은 [API 가이드](api/README.md)와 [스키마](src/cosmetic_agent/domain/schemas.py)를 참고하세요.

## 8. 테스트와 평가 재현

### Django 웹 서비스

저장소 루트에서 시작합니다. 웹 테스트는 AI 서버를 대역으로 처리하며, 실제 OpenAI·Qdrant 호출 없이 실행합니다.

```powershell
cd web
uv run python manage.py test
cd ..
```

제품·실증 자료 변환, 사용자별 접근 제한, 검토·생성 이력 저장, AI 오류 처리, 챗봇 메시지·맥락 저장, 회원가입과 페이지 렌더링, 운영 DB 설정 및 readiness를 검사합니다. 실제 RDS·AI 서버 연동과 배포 후 로그인·이력 유지 확인은 [배포 가이드](docker/README.django.md)에 따라 별도로 수행합니다.

### AI 엔진 회귀와 평가

저장소 루트에서 실행합니다.

```powershell
# 단위·통합 회귀 테스트
uv run pytest

# 규칙 기반 사전 판정 평가
uv run python -m eval.run_eval --backend rule --split dev

# GPT 비교 평가 (외부 API 호출)
uv run python -m eval.run_eval --backend rule gpt gpt-few --split dev

# 실제 인덱스의 검색 평가 (OpenAI·Qdrant 연결 필요)
uv run python scripts/validate_rag.py --split dev

# 고정 holdout 회귀셋의 검색 평가
uv run python scripts/validate_rag.py --split holdout --confirm-holdout
```

테스트는 규칙 판정·기능성 예외·수치 검증·응답 계약·검색 결합·재시도 상한·생성·챗봇·UI 연결·매출 시나리오를 다룹니다. 테스트용 서비스나 대역을 주입한 검증은 실제 외부 모델의 품질 평가와 구분합니다. 판정 평가의 세부 조건은 [평가 가이드](eval/README.md)에 정리했습니다.

## 9. 디렉토리 구조

```text
├── api/                       # FastAPI 라우트·요청 처리
├── web/                       # 4차 Django 웹 서비스 (별도 uv 프로젝트)
│   ├── config/                # Django 설정·URL·WSGI
│   ├── core/                  # 홈·AI 클라이언트·DB 준비 상태 점검
│   ├── accounts/              # 회원가입·로그인·로그아웃
│   ├── products/              # 사용자별 제품·실증 자료
│   ├── reviews/               # 검토·생성 요청과 이력
│   ├── chat/                  # 대화방·메시지·대화 맥락
│   ├── templates/             # Django HTML 템플릿
│   └── static/                # CSS·JavaScript
├── app/                       # 기존 Streamlit 참고 앱
├── configs/                   # 판정·검색·재시도 설정
├── data/
│   ├── 01_raw/                # 규정·사례·원료성분 원본
│   ├── 02_processed/          # 조항 청크·BM25 인덱스
│   ├── assets/                # 규칙·표현 단계·제품 자산
│   ├── golden_set/            # 팀 작성 판정 벤치마크
│   ├── ingredient_knowledge/  # 성분 참고 지식
│   ├── market_reference/      # 시장 제품·문구 참고
│   ├── copy_bank/             # 표현 은행
│   └── sales_forecast_reference/ # 시나리오·공개 비교 실험 자료
├── indexing/                  # 원문 청킹·메타데이터·색인 생성
├── src/cosmetic_agent/
│   ├── common/                # 환경설정·로깅·예외
│   ├── domain/                # 스키마·규칙·실증 검증
│   ├── rag/                   # Dense·BM25·RRF·reranker
│   ├── models/                # 판정·교정·생성·챗봇 모델
│   ├── workflow/              # 검토 LangGraph
│   ├── generation/            # 생성 LangGraph
│   └── service.py             # 검토 서비스 진입점
├── eval/                      # 판정 평가·저장 보고서
├── tests/                     # 단위·통합 테스트
├── scripts/                   # 데이터 구축·검색 평가·배포 보조
├── docker/                    # API·웹 이미지, Caddy, 운영 환경변수·배포 안내
├── docker-compose.web.yml     # 4차 Django + FastAPI + Caddy 배포
├── docker-compose.yml         # 기존 FastAPI + Streamlit 실행
├── docs/                      # 참고 화면·다이어그램·이전 계획서
├── finetune/                  # 향후 파인튜닝 실험 골격
└── plan.md                    # 4차 역할 분담·일정·테스트 계획
```

## 10. 한계와 개선 방향

- **파인튜닝**: `finetune/`은 QLoRA 실험용 골격이며, 학습 완료 모델이나 검증된 성능을 제공하는 상태는 아닙니다. 실행에는 `JUDGE_BACKEND=rule` 또는 구현된 GPT 백엔드를 사용합니다.
- **검증 범위**: AI 평가 수치는 기존 소규모 평가셋의 저장 결과입니다. 새로운 독립 평가셋과 전문가 검토, Django·RDS·실제 AI 서버를 연결한 통합 검증을 추가해야 합니다.
- **복합 실증**: 현재 효능 감지는 키워드에 의존합니다. 시험 자료를 효능·시점·대상·수치로 구조화해 복합 주장의 대응 관계를 정밀하게 검증하는 것이 다음 과제입니다.
- **규정 갱신**: 수집된 문서 버전에 의존합니다. 개정 감지, 효력 시점 관리, 재색인 절차를 고도화할 필요가 있습니다.
- **생성 품질**: 코드 검증 통과가 모든 광고 표현의 적합성을 보장하지 않습니다. 검증 실패 후보의 최종 노출 차단과 생성·인용 품질 평가는 4차 개선 항목입니다.
- **시장 성과**: 다른 분야의 공개 문구 실험을 화장품 매출 상승률로 일반화하지 않습니다. 실제 광고 A/B 실험과 성과 데이터가 필요합니다.
- **화면 확장**: Django 웹에는 회원·제품·검토·생성·이력·챗봇 화면이 구현되어 있습니다. 기존 상세페이지 일괄 검토·규정 열람·시장 비교·매출 시나리오 화면 이식은 추가 작업입니다.
- **운영 고도화**: 회원별 DB 저장과 배포 구성은 구현되어 있습니다. 운영 환경에서 백업·복구, 장애 관측, 감사 로그, 부하·응답 시간 검증을 확장할 수 있습니다.

협업은 담당자 브랜치에서 개발한 뒤 `dev`·`main`으로 통합하는 방식으로 진행했습니다. 데이터 출처·이용 조건은 각 데이터 README에, 상세 역할 계획은 [plan.md](plan.md)에 기록되어 있습니다.
