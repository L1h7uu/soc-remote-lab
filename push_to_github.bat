@echo off
title Push SOC Remote Lab to GitHub
echo ========================================================
echo   Pushing SOC Remote Lab to https://github.com/L1h7uu/soc-remote-lab
echo ========================================================
echo.

set /p TOKEN="Nhap GitHub Personal Access Token (hoac an Enter neu da dang nhap GCM): "

if "%TOKEN%"=="" (
    echo Dang day code len GitHub qua Git Credential Manager...
    git push -u origin main
) else (
    echo Dang day code len bang Token...
    git push -u https://%TOKEN%@github.com/L1h7uu/soc-remote-lab.git main
)

echo.
if %ERRORLEVEL% equ 0 (
    echo [OK] Push thanh cong len https://github.com/L1h7uu/soc-remote-lab!
) else (
    echo [!] Push that bai. Kiem tra xem ban da tao repo 'soc-remote-lab' tren GitHub chua.
)
pause
