Run the script with the path to either a single MTL file or a directory.

If the path is a directory, it will scan all MTL files in that directory (including subfolders if the -s flag is provided).
If the path is a file, it will only scan that specific MTL file.

you can run the script with the -f or --save_file flag to save the list of missing textures to a file.

If you want to provide a custom name and location for the file, you can specify it after the flag.

If no custom name and location are provided, the script will save the file in the MTL directory with the default name "missing_textures.txt".

Here are some example usages:

Scan all MTL files in a directory (including subfolders):
python script.py /path/to/mtl_directory -s

Scan a single MTL file:
python script.py /path/to/single_mtl_file.mtl

Scan all MTL files in a directory (including subfolders) and save missing textures to a file named "custom_name.txt" in the MTL directory:
python script.py /path/to/mtl_directory -s -f custom_name.txt

Scan all MTL files in a directory (including subfolders) and save missing textures to a file named "custom_name.txt" in a different directory:
python script.py /path/to/mtl_directory -s -f /path/to/save_directory/custom_name.txt

Scan all MTL files in a directory (including subfolders) and save missing textures to the default file "missing_textures.txt" in the MTL directory:
python script.py /path/to/mtl_directory -s -f

In these examples, /path/to/mtl_directory should be replaced with the actual path to your MTL directory.
The -s flag indicates that the script should scan all subfolders within the MTL directory.

After running the script, it will display the missing textures along with the associated MTL files.
If the -f flag is provided, it will save the missing textures to the specified file.
If no custom name and location are provided, it will save the file in the MTL directory with the default name "missing_textures.txt".