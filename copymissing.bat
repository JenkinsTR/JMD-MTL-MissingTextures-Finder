@ECHO OFF

REM Get the directory of the batch file
SET "TOOL_DIR=K:\GitHub\JMD-MTL-MissingTextures-Finder"
SET "MTL_DIR=%~dp0"
SET "OUTPUT_DIR=C:\path\to\output_directory"

REM Copy the textures to a chosen output directory without updating the original MTL files
python "%TOOL_DIR%\mtl_texture_management.py" "%MTL_DIR%" -c -o "%OUTPUT_DIR%"

PAUSE
EXIT
