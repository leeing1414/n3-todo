#!/bin/sh
set -e

if [ ! -f .env ]; then
  echo "[INFO] .env 파일이 없습니다. .env.example을 기반으로 생성하세요." >&2
  exit 1
fi

if [ ! -f web/.env ]; then
  echo "[INFO] web/.env 파일이 없습니다. web/.env.example을 기반으로 생성하세요." >&2
  exit 1
fi

docker compose up --build -d

echo "[INFO] 개발 서버가 백그라운드에서 실행 중입니다."
echo "  - FastAPI API: http://localhost:8000/docs"
echo "  - React 클라이언트: http://localhost:5173"
