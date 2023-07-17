@echo off

REM Get the directory of the batch file
SET "WORK_DIR=%~dp0"

SET "MTL_DIR=W:\GTA\2008 - Grand Theft Auto IV\_GAME\_DECOMPILED"
SET "OUT_DIR=W:\GTA\2008 - Grand Theft Auto IV\_GAME\_DDS"
SET "MISSINGTXT=%WORK_DIR%\missing_textures.txt"

python "%WORK_DIR%\retrieve_missing.py" -i "%MTL_DIR%" -m "%MISSINGTXT%" -o "%OUT_DIR%"

PAUSE
EXIT
