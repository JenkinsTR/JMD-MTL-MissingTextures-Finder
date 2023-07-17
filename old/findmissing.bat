@echo off

REM Get the directory of the batch file
SET "WORK_DIR=%~dp0"
SET "MTL_DIR=W:\GTA\2008 - Grand Theft Auto IV\_GAME\_DECOMPILED"

python "%WORK_DIR%\script.py" "%MTL_DIR%" -s -f "%WORK_DIR%\missing_textures.txt"

PAUSE
EXIT
