@echo off
cd /d "%~dp0"
echo.
echo ========================================
echo   GITHUB CRAWLER - WINDOWS LOCAL RUN
echo ========================================
echo.

echo [1] Starting Postgres...
docker start mypg 2>nul || docker run -d --name mypg -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:15

echo.
echo [2] Installing packages (pg8000 = no compile)...
pip install -r requirements.txt --no-cache-dir

echo.
echo [3] Creating table...
docker cp sql/init.sql mypg:/init.sql
docker exec -it mypg psql -U postgres -d postgres -f /init.sql

echo.
echo [4] Crawling 100,000 repos...
python crawler/main.py

echo.
echo [5] Exporting CSV...
python dump_csv.py

echo.
echo ========================================
echo   SUCCESS! Opening repos.csv
echo ========================================
timeout /t 3 >nul
start "" "repos.csv"
pause