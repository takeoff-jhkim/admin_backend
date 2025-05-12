# Admin Backend Project

관리자 페이지 백엔드 시스템 구축을 위한 FastAPI + PostgreSQL + Alembic + Docker 기반 프로젝트입니다.

---

## 📦 기술 스택
- **Python 3.12**
- **FastAPI**
- **PostgreSQL (Docker)**
- **Alembic** (DB 마이그레이션)
- **SQLAlchemy** (ORM)
- **Pydantic v2** (데이터 검증)
- **Passlib + JWT** (암호화 및 인증)
- **Docker Compose** (개발 환경 구성)

---

## 📁 디렉토리 구조
```bash
├── alembic/              # Alembic 마이그레이션 관련 설정 및 버전 파일
│   ├── versions/         # 개별 마이그레이션 스크립트 저장소
│   ├── env.py            # Alembic 환경설정 (DB 연결 등)
│   ├── README            # Alembic 사용법 정리 문서
│   └── script.py.mako    # 마이그레이션 스크립트 템플릿
│
├── app/                  # FastAPI 애플리케이션 폴더
│   ├── main.py           # FastAPI 진입점
│   ├── models.py         # SQLAlchemy 모델 정의
│   ├── schemas.py        # Pydantic 스키마 정의
│   ├── crud.py           # DB 조작 로직
│   ├── database.py       # DB 연결 및 Base 설정
│   ├── config.py         # 설정 값 로딩
│   ├── utils/            # 인증 및 보안 유틸리티 함수
│   │   └── security.py
│   └── routers/          # API 라우팅 정의
│       └── admin.py
│
├── .env.sample           # 환경 변수 예시 파일
├── .gitignore            # Git에 추적되지 않아야 할 파일들
├── requirements.txt      # 의존성 패키지 목록
├── Dockerfile            # Docker 빌드 스크립트
├── compose.yaml          # Docker Compose 설정
└── alembic.ini           # Alembic 설정 파일
```

---

## 🚀 실행 방법 (Docker 기반)
```bash
# 개발용 환경 변수 복사
cp .env.dev .env

# 도커 빌드 및 실행
docker compose up --build

# 실행 중지
docker compose down
```

### 🐳 도커 환경에서 확인할 것
- `localhost:8000/docs` (Swagger UI)
- 개발용 DB는 컨테이너 내부 PostgreSQL 사용

---

## 🔐 인증 방식: JWT 기반
- `/admin/login`에서 로그인 → 토큰 발급
- 토큰을 Swagger Authorize 또는 Postman 헤더에 `Authorization: Bearer <token>` 형식으로 전달해야 인증 API 접근 가능
- 인증된 사용자만 `/admin/users` 등 주요 API 접근 가능

```python
# 인증된 사용자만 접근하는 예시
@router.get("/users")
def get_users(current_user: User = Depends(get_current_user)):
    ...
```

---

## 🧱 Alembic 마이그레이션
### 마이그레이션 파일 생성
```bash
PYTHONPATH=. alembic revision --autogenerate -m "변경내용 설명"
```

### DB에 적용
```bash
PYTHONPATH=. alembic upgrade head
```

### 롤백
```bash
PYTHONPATH=. alembic downgrade <revision_id>
```

> `alembic/versions` 안의 마이그레이션 파일은 반드시 커밋해야 합니다.

---

## 🧪 개발용 환경 변수 파일
- `.env.dev`, `.env.prod`은 **절대 커밋하지 않습니다**.
- 개발 및 운영 환경에 따라 분리된 `.env` 사용
- 예시 파일 `.env.sample` 참고

🔐 **실제 `.env.dev`, `.env.prod` 내용이 필요하다면 팀원 @jhkim 에게 직접 요청하세요.**

---

## 🧑‍🤝‍🧑 팀 협업 시
1. 깃 클론
```bash
git clone https://github.com/<owner>/<repo>.git
cd admin_backend
```
2. `.env.dev` 파일을 받아 복사
```bash
cp .env.dev .env
```
3. 도커 실행
```bash
docker compose up --build
```

---

## ✅ Git 커밋 시 포함 항목
- `app/`
- `alembic/` (env.py, script.py.mako, versions/ 등 포함)
- `.gitignore`, `Dockerfile`, `compose.yaml`, `requirements.txt`, `.env.sample`

❌ 커밋하지 않는 항목
- `__pycache__/`, `.env.dev`, `.env.prod`, `.pyc`, `env/` (가상환경)

---

## 💡 기타
- `SECRET_KEY`, `ALGORITHM` 등은 `.env` 파일에서 관리하고, 코드 내에서는 `os.getenv`로 불러옵니다.
- `alembic_version` 테이블은 Alembic이 생성하며 삭제하면 안됩니다.
- 모든 인증이 필요한 API는 `Depends(get_current_user)`로 보호됩니다.

---

> 작성자: @jhkim


## 🚀 향후 과제

- 관리자 화면 연동 (Next.js 등)
- CI/CD 설정 (GitHub Actions)
- OAuth 등 소셜 로그인 연동

