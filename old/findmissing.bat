@ECHO OFF

REM Get the directory of the batch file
SET "TOOL_DIR=K:\GitHub\JMD-MTL-MissingTextures-Finder"
SET "MTL_DIR=%~dp0"

python "%TOOL_DIR%\script.py" "%MTL_DIR%" -s -f "%MTL_DIR%\missing_textures.txt"

PAUSE
EXIT
