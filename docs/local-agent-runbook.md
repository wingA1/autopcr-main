# Local Agent Runbook

This file is only for me (Codex agent) to speed up future runs in this repo.

## Quick Start

### 1) Backend (existing conda env)

- Conda env name: autopcr
- Start command:

```powershell
conda run -n autopcr --cwd "D:/Desktop/things/autopcr-main" python _httpserver_test.py
```

- Expected backend URL: http://localhost:13200
- Health check: TCP port 13200 should be listening.

### 2) Frontend (Node)

- Frontend app path: AutoPCR_Web
- Env file: AutoPCR_Web/.env

```env
AUTOPCR_SERVER_HOST=http://localhost:13200
AUTOPCR_WEBUI_LISTEN=localhost
```

- Install dependencies only if node_modules is missing:

```powershell
cd "D:/Desktop/things/autopcr-main/AutoPCR_Web"
npm install
```

- Start dev server:

```powershell
cd "D:/Desktop/things/autopcr-main/AutoPCR_Web"
$env:BROWSER="none"
npm run dev
```

- Expected frontend URL: http://localhost:5173/daily
- Health check: TCP port 5173 should be listening.

## Notes for Me

- The repo already contains AutoPCR_Web, which is the frontend.
- pyproject.toml says project Python is >=3.10,<3.11, but user already has a working conda env named autopcr. I must not recreate or replace it.
- If frontend .env is missing, create it before npm run dev.
- If backend port 13200 is busy, ask user before changing port.
- Do not run git commit/push unless explicitly asked.

## Useful Checks

```powershell
Test-NetConnection 127.0.0.1 -Port 13200
Test-NetConnection ::1 -Port 5173
Get-NetTCPConnection -State Listen | Where-Object { $_.LocalPort -in 13200,5173 }
```

## Known Behaviors

- Backend may take a few seconds to bind port.
- Frontend Vite server may bind to IPv6 ::1 first; use ::1 in TCP check if 127.0.0.1 fails.
