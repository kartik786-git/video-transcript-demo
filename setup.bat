@echo off
setlocal
cd /d "%~dp0"

echo ============================================
echo  transcript-video  one-time setup
echo ============================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo  ERROR: Python not found on PATH.
    echo  Install Python 3.10+ from https://python.org and tick "Add to PATH".
    echo.
    goto :err
)

echo [1/3] Creating virtual environment...
if exist ".venv\Scripts\python.exe" (
    echo  .venv already exists - reusing it.
) else (
    python -m venv .venv || goto :err
)
call ".venv\Scripts\activate.bat" || goto :err

echo [2/3] Installing dependencies...
python -m pip install --upgrade pip >nul
pip install -r requirements-web.txt || goto :err

echo [3/3] Downloading Whisper models (needed once; works offline afterwards)...
python download_model.py --size small medium || goto :err

echo.
echo  Verifying installed packages...
".venv\Scripts\python.exe" -c "import faster_whisper, yt_dlp, youtube_transcript_api, streamlit, pandas; print('  OK - all dependencies importable.')" || goto :err

echo.
echo ============================================
echo  Setup complete. No token or account needed.
echo.
echo  To launch the web app, double-click:
echo      run_webapp.bat
echo  ...or run:
echo      .venv\Scripts\streamlit.exe run webapp.py
echo.
echo  To transcribe a file or URL from the CLI:
echo      run_cli.bat my_video.mp4
echo  ...or run:
echo      .venv\Scripts\python.exe app.py my_video.mp4
echo ============================================
echo.
choice /c YN /n /m "Launch the web app now? [Y/N] "
if errorlevel 2 goto :eof
".venv\Scripts\streamlit.exe" run webapp.py
goto :eof

:err
echo.
echo Setup FAILED. Check the message above.
pause
exit /b 1
