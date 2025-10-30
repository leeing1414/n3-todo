# N3 Todo Collaboration Platform

사내 프로젝트 · 태스크 · 서브태스크를 계층 구조로 관리하는 통합 업무 플랫폼의 백엔드(FastAPI)와 프론트엔드(React + Tailwind + Zustand) 구현입니다. 개발 계획서.md의 요구사항을 따라 대시보드, 칸반, 간트, 캘린더, 데이터 그리드, 활동 로그, 개인 업무 패널을 포함했습니다.

## 📦 프로젝트 구조

`
├─ app/                # FastAPI 애플리케이션
│  ├─ base/            # 공통 응답/도큐먼트 베이스
│  ├─ core/            # 설정 및 환경 변수 정의
│  ├─ collections/     # MongoDB 컬렉션 어댑터
│  ├─ documents/       # 도메인 데이터 클래스
│  ├─ requests/        # Pydantic 요청 모델
│  ├─ responses/       # API 응답 래퍼
│  ├─ routers/         # FastAPI 라우터(인증, 프로젝트, 태스크 등)
│  ├─ services/        # 비즈니스 로직과 대시보드 집계
│  └─ utils/           # 보안/직렬화 유틸리티
│
├─ web/                # React + Vite 프론트엔드
│  ├─ public/styles    # @n3-web-origin CSS 반영
│  ├─ src/components   # 대시보드, 레이아웃, 칸반, 간트 등 UI 컴포넌트
│  ├─ src/store        # Zustand 전역 상태 및 API 연동
│  └─ src/types        # 백엔드 DTO와 동기화된 타입 정의
├─ requirements.txt    # 백엔드 의존성
└─ README.md           # 실행 가이드(현재 문서)
`

## ⚙️ 백엔드 실행 방법 (FastAPI)

1. Python 3.11 이상이 설치되어 있는지 확인한 뒤 Pipenv 가상 환경을 생성합니다.

   `ash
   pipenv install
   `

   > pipenv install --dev 를 실행하면 타입 힌트용 dev 패키지까지 함께 설치됩니다.  
   > 기존 방식이 필요하면 pip install -r requirements.txt 도 사용할 수 있습니다.

2. 환경 변수를 설정합니다. 제공된 예시 파일을 복사해 사용하세요.

   `ash
   cp .env.example .env
   `

   `env
   MONGO_DB_URL=mongodb://localhost:27017
   MONGO_DB_NAME=n3_todo
   MODE=local
   JWT_SECRET_KEY=replace-with-strong-secret
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   `

3. 개발 서버를 실행합니다.

   `ash
   pipenv run start
   `

5. 브라우저에서 http://localhost:8000/docs 로 접근해 OpenAPI 문서를 확인할 수 있습니다.

## 🖥️ 프론트엔드 실행 방법 (React + Vite)

1. web 디렉터리로 이동합니다.

   `ash
   cd web
   `

2. 패키지를 설치합니다. (npm 또는 pnpm 사용 가능)

   `ash
   npm install
   `

3. 환경 변수를 설정합니다. 예시 파일을 복사하거나 직접 web/.env 파일을 생성합니다.

   `ash
   cp web/.env.example web/.env
   `

   `env
   VITE_API_BASE_URL=http://localhost:8000
   `

4. 개발 서버를 실행합니다.

   `ash
   npm run dev
   `

5. 브라우저에서 http://localhost:5173 에 접속하면 Tailwind와 @ne-web-origin CSS가 적용된 대시보드 UI를 확인할 수 있습니다.

## 🐳 Docker Compose 개발 환경

로컬 툴 체인을 직접 설치하지 않고도 하나의 명령으로 MongoDB · FastAPI · Vite 개발 서버를 동시에 띄울 수 있습니다.

1. 환경 변수 파일을 준비합니다.

   `ash
   cp .env.example .env
   cp web/.env.example web/.env
   `

   > Docker Compose에서는 백엔드가 자동으로 mongodb://mongo:27017 을 바라보므로 .env 의 MONGO_DB_URL 을 기본값 그대로 두어도 됩니다.

2. Docker Compose를 실행합니다.

   `ash
   docker compose up --build
   `

   - ackend 컨테이너: uvicorn --reload 로 FastAPI를 8000 포트에서 제공  
   - rontend 컨테이너: 
pm run dev -- --host 0.0.0.0 --port 5173 로 Vite 개발 서버 제공  
   - mongo 컨테이너: MongoDB 7.x

3. 브라우저에서 다음 주소로 접속합니다.

   - API 문서: [http://localhost:8000/docs](http://localhost:8000/docs)  
   - 웹 클라이언트: [http://localhost:5173](http://localhost:5173)

4. 컨테이너 로그를 중지하려면 Ctrl + C, 완전 종료는 docker compose down 을 사용하세요.

### ⏯️ 스크립트로 빠르게 제어하기

- 개발 서버 기동: ./start_dev.sh (실행 전 .env, web/.env 가 준비되어 있어야 합니다)  
- 개발 서버 종료: ./end_dev.sh

## 🧩 주요 기능 요약

- **조직 계층 관리**: 회사 · 부서 · 사용자 엔티티와 RBAC 준비된 JWT 인증 토대 제공
- **프로젝트 도메인**: 프로젝트/태스크/서브태스크 CRUD, 활동 로그, 통계 API
- **대시보드 집계**: 상태/부서 분포, 마감 임박/지연 업무, 최근 활동, AI 요약 섹션 플레이스홀더
- **프론트 UI**: Recharts 기반 차트, @hello-pangea/dnd 칸반, frappe-gantt 간트, FullCalendar 캘린더, TanStack Table 그리드, 개인 업무 패널
- **스타일링**: Tailwind 유틸리티와 @ne-web-origin CSS를 조합해 내부 디자인 가이드 반영

## ✅ 향후 확장 아이디어

- JWT 기반 세션과 역할 권한 매핑 완성, 실사용자 연동
- 태스크 드래그 드롭 결과를 API로 반영하는 상태 저장
- AI 요약/우선순위 추천, CSV/Excel 내보내기, 실시간 알림(WebSocket/SSE)
- 종합 테스트 코드 및 CI 파이프라인 보강

필요한 추가 요구 사항이 있으면 언제든지 알려주세요!
