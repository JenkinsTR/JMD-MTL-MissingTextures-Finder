# MTL Texture Management Script

- [Requirements](#requirements)
- [Usage](#usage)
- [Functionalities](#functionalities)
  - [Finding Missing Textures](#finding-missing-textures)
  - [Locating the Largest Versions of Textures](#locating-the-largest-versions-of-textures)
  - [Updating the MTL Files](#updating-the-mtl-files)
  - [Creating Backup Copies](#creating-backup-copies)
  - [Supported Texture Types](#supported-texture-types)
- [Examples](#examples)
- [License](#license)

This script is designed to help with managing textures in MTL files. It provides various functionalities, including finding missing textures, locating the largest versions of the textures, and updating the MTL files with the new texture paths. Additionally, it supports copying the textures to a chosen folder.

## Requirements

- Python 3.x

## Usage

1. Ensure you have the necessary requirements mentioned above.

2. Download the script file to your computer.

3. Open a terminal or command prompt and navigate to the directory where the script is saved.

4. Run the following command to see the available options and arguments:

    ```
    python mtl_texture_management.py -h
    ```

    This will display the help message with all the available options and their explanations.

5. Run the script with the desired options and arguments. Here are a few examples:

    - To find missing textures without extensions in the MTL directory and its subfolders, and save the information to a file named `missing_textures.txt`:

        ```
        python mtl_texture_management.py -i /path/to/mtl_directory -s -f
        ```

    - To copy the textures to a chosen output directory without updating the original MTL files:

        ```
        python mtl_texture_management.py -i /path/to/mtl_directory -c -o /path/to/output_directory
        ```

    - To find missing textures and update the MTL files with the new texture paths without copying the textures:

        ```
        python mtl_texture_management.py -i /path/to/mtl_directory -u
        ```

    - To find missing textures, locate the largest versions, and update the MTL files, leaving the original MTL files untouched:

        ```
        python mtl_texture_management.py -i /path/to/mtl_directory -u -L
        ```

    - To find missing textures, create backup copies of the original MTL files, locate the largest versions, and update the MTL files:

        ```
        python mtl_texture_management.py -i /path/to/mtl_directory -u -b -L
        ```

    - To find missing textures, create backup copies of the original MTL files, locate the largest versions, copy the textures to a chosen output directory, and update the MTL files:

        ```
        python mtl_texture_management.py -i /path/to/mtl_directory -u -b -L -c -o /path/to/output_directory
        ```

    - To find missing textures and locate the largest versions without modifying the MTL files:

        ```
        python mtl_texture_management.py -i /path/to/mtl_directory -L
        ```

    Note: 
    - Replace `/path/to/mtl_directory` with the actual path to your MTL directory.
    - The `MTL_DIR` variable in the batch files is set to the directory where the batch file is launched from. You don't need to modify it.
    - The `TOOL_DIR` variable in the batch files should be updated with the directory path to where the python script is saved. Modify it accordingly in each batch file.
    - The `OUTPUT_DIR` variable in the batch files should be updated with the desired output directory path. Modify it accordingly in each batch file.

## Functionalities

### Finding Missing Textures

The script can search for missing textures without extensions in the MTL files. It scans the specified directory and its subfolders (if `-s` option is used) to locate the missing textures. The information about missing textures is printed to the console and can be saved to a text file using the `-f` option. By default, the file is named `missing_textures.txt` and saved in the MTL directory.

### Locating the Largest Versions of Textures

The script determines the largest versions of the textures in the MTL directory and its subfolders. It compares the file sizes of textures with the same name and selects the largest one. The `-L` option allows finding the largest versions of the textures. If not specified, the script uses the first encountered texture.

### Updating the MTL Files

The script can update the original MTL files with the new texture paths. If the `-u` option is used, it modifies the MTL files by replacing the original texture paths with the paths of the largest versions of the textures. The updated MTL files are saved with the new texture paths.

By default, the script only prints the changes without modifying the files. Use the `-u` option to enable the update functionality.

### Creating Backup Copies

The script can create backup copies of the original MTL files before modifying them. If the `-b` option is used, it creates backup copies of the MTL files with the extension '.mtlbkp'. The backup files are saved alongside the original MTL files.

### Supported Texture Types

The script supports the following types of textures that can be defined in the .mtl file:

- map_Ka: Ambient texture
- map_Kd: Diffuse texture
- map_Ks: Specular texture
- map_Ns: Specular highlight texture
- map_d: Dissolve texture
- map_bump: Bump texture
- bump: Bump texture
- disp: Displacement texture
- decal: Decal texture

## Examples

Here are some example scenarios and how to use the script for each:

1. Finding Missing Textures:

    Suppose you want to identify missing textures without extensions in the MTL directory and its subfolders. You also want to save the information to a file named `missing_textures.txt` in the MTL directory. Run the following command:

    ```
    python mtl_texture_management.py -i /path/to/mtl_directory -s -f
    ```

    This will search for missing textures, display them on the console, and save the information to `missing_textures.txt`.

2. Copying Textures:

    Suppose you want to copy the largest versions of the textures to a chosen output directory without modifying the original MTL files. Run the following command:

    ```
    python mtl_texture_management.py -i /path/to/mtl_directory -c -o /path/to/output_directory
    ```

    This will locate the largest versions of the textures and copy them to the specified output directory.

3. Updating MTL Files:

    Suppose you want to update the original MTL files with the new texture paths but not copy the textures. Run the following command:

    ```
    python mtl_texture_management.py -i /path/to/mtl_directory -u
    ```

    This will search for missing textures, locate the largest versions, and update the original MTL files with the new texture paths.

4. Finding Missing Textures, Creating Backup Copies, Locating the Largest Versions, Copying Textures, and Updating MTL Files:

    Suppose you want to perform all the tasks together - find missing textures, locate the largest versions, and update the MTL files. Additionally, you want to copy the largest textures to a chosen output directory. Run the following command:

    ```
    python mtl_texture_management.py -i /path/to/mtl_directory -u -b -L -c -o /path/to/output_directory
    ```

    This will search for missing textures, display them, create backup copies of the original MTL files, locate the largest versions, update the MTL files, and copy the largest textures to the specified output directory.

5. Finding Missing Textures and Locating the Largest Versions:

    Suppose you want to find missing textures and locate the largest versions without modifying the MTL files. Run the following command:

    ```
    python mtl_texture_management.py -i /path/to/mtl_directory -L
    ```

    This will search for missing textures, display them, and locate the largest versions of the textures.

6. Using `listmissing.bat`:

    The `listmissing.bat` batch file is provided for your convenience. It performs the task of finding missing textures without extensions in the MTL directory and its subfolders, and saves the information to a file named `missing_textures.txt`. To use it, simply run the following command:

    ```
    listmissing.bat
    ```

    Note: Before using the `listmissing.bat` file, ensure that you update the `TOOL_DIR` variable in the batch file with the folder where the python script is saved.

7. Using `copymissing.bat`:

    The `copymissing.bat` batch file is provided for your convenience. It performs the task of copying the textures to a chosen output directory without updating the original MTL files. To use it, simply run the following command:

    ```
    copymissing.bat
    ```

    Note: Before using the `copymissing.bat` file, ensure that you update the `TOOL_DIR` variable in the batch file with the folder where the python script is saved and `OUTPUT_DIR` variable in the batch file with your desired output directory path.

8. Using `updatemissing.bat`:

    The `updatemissing.bat` batch file is provided for your convenience. It performs the task of finding missing textures, creating backup copies of the original MTL files, locating the largest versions, and updating the MTL files. To use it, simply run the following command:

    ```
    updatemissing.bat
    ```

    Note: Before using the `updatemissing.bat` file, ensure that you update the `TOOL_DIR` variable in the batch file with the folder where the python script is saved.

9. Using `list+copy+update_missing.bat`:

    The `list+copy+update_missing.bat` batch file is provided for your convenience. It performs all the tasks together - finding missing textures, creating backup copies of the original MTL files, locating the largest versions, copying the textures to a chosen output directory, and updating the MTL files. To use it, simply run the following command:

    ```
    list+copy+update_missing.bat
    ```

    Note: Before using the `list+copy+update_missing.bat` file, ensure that you update the `TOOL_DIR` variable in the batch file with the folder where the python script is saved and `OUTPUT_DIR` variable in the batch file with your desired output directory path.


Feel free to customize and enhance the script to fit your specific requirements.

## License

This script is provided under the [MIT License](LICENSE).

---

&copy; 2023 JMDigital | Version 1.3  
Website: [jmd.vc](https://jmd.vc)
