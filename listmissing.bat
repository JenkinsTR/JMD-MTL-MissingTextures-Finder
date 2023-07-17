@ECHO OFF

REM Get the directory of the batch file
SET "TOOL_DIR=K:\GitHub\JMD-MTL-MissingTextures-Finder"
SET "MTL_DIR=%~dp0"

REM Find missing textures without extensions in the MTL directory and its subfolders, and save the information to a file named missing_textures.txt
python "%TOOL_DIR%\mtl_texture_management.py" "%MTL_DIR%" -s -f "%MTL_DIR%\missing_textures.txt"

PAUSE
EXIT
