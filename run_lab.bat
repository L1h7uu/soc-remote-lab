@echo off
title SOC Remote Lab Launcher
echo ========================================================
echo   KHOI DONG SOC REMOTE INVESTIGATION LAB
echo ========================================================
echo.

echo [*] Dang khoi dong container lab (Docker)...
docker compose up -d

echo.
echo [*] Lab dang chay tai: http://localhost:7681
echo [*] Tai khoan dang nhap: guest / Demo@123
echo.
echo ========================================================
echo   MO LINK TRUY CAP TU XA QUA CLOUDFLARE TUNNEL
echo ========================================================
echo Dang bat tunnel... Vui long copy link https://*.trycloudflare.com ben duoi vao CV:
echo.

cloudflared tunnel --url http://localhost:7681
pause
