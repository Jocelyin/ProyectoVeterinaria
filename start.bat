@echo off
echo ==========================================
echo  VeterinariaTest - Iniciando servicios...
echo ==========================================

echo.
echo [1/2] Iniciando Backend (FastAPI)...
start "Backend - FastAPI" cmd /k "cd /d %~dp0backend && uvicorn api:app --reload"

timeout /t 2 /nobreak >nul

echo [2/2] Iniciando Frontend (Astro)...
start "Frontend - Astro" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ==========================================
echo  Servicios iniciados!
echo  Backend:  http://localhost:8000
echo  Frontend: http://localhost:4321
echo ==========================================
echo.
pause
