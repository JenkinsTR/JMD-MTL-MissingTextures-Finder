# Import required modules
import os
import re
import shutil
import argparse
import glob
import multiprocessing

# ==============================================================================
# COPYRIGHT INFORMATION
# ==============================================================================
#
# This script is developed by JMDigital (https://jmd.vc) - Version 1.3 (07.2023)
#
# ==============================================================================

# Define ANSI escape codes for colors
colors = {
    "red": "\033[91m",
    "green": "\033[92m",
    "orange": "\033[93m",
    "blue": "\033[94m",
    "reset": "\033[0m"
}

# Updated regular expression pattern to capture texture type and name without extensions
texture_pattern = r"(" + "|".join(rf"(?:{texture_type})" for texture_type in ["map_Ka", "map_Kd", "map_Ks", "map_Ns", "map_d", "map_bump", "bump", "disp", "decal"]) + r")\s+(\b(?!\.).+\b)"

# Function to find the largest texture path
def find_largest_texture(mtl_directory, texture_name, find_largest):
    largest_texture_size = 0
    largest_texture_path = ""

    # Iterate over texture files in the MTL directory and its subfolders
    for root, _, filenames in os.walk(mtl_directory):
        for filename in filenames:
            if texture_name.lower() in filename.lower():
                texture_path = os.path.join(root, filename)
                if find_largest:
                    texture_size = os.path.getsize(texture_path)
                    if texture_size > largest_texture_size:
                        largest_texture_size = texture_size
                        largest_texture_path = texture_path
                else:
                    return texture_path

    return largest_texture_path

# Function to find the texture path with different extensions
def find_texture_path(mtl_directory, texture_name, texture_extensions):
    # Iterate over supported extensions to find the texture path
    for extension in texture_extensions:
        texture_path = find_largest_texture(mtl_directory, texture_name + extension, find_largest=True)
        if texture_path:
            return texture_path

    return None


# Helper function to get the subfolder path for copying the largest texture
def get_subfolder_path(mtl_file):
    mtl_filename = os.path.splitext(mtl_file)[0]
    subfolder_path = os.path.join(os.path.dirname(mtl_file), mtl_filename)
    return subfolder_path

# Function to find missing textures in MTL files and save to a text file
def find_missing_textures(mtl_directory, scan_subfolders, save_file, fast_mode):
    # Helper function to check if the file is an MTL file
    def is_mtl_file(filename):
        return filename.lower().endswith(".mtl")

    # List of supported texture extensions
    texture_extensions = [".dds", ".png", ".jpg", ".jpeg", ".tga", ".bmp", ".gif", ".tif"]

    # Initialize the list to store missing textures
    all_missing_textures = []

    # Iterate over MTL files in the directory and its subfolders if required
    for root, _, filenames in os.walk(mtl_directory):
        if scan_subfolders or root == mtl_directory:
            for filename in filenames:
                if is_mtl_file(filename):
                    filepath = os.path.join(root, filename)
                    backup_path = filepath + "bkp"  # Backup path for .mtlbkp file
                    print("----------------------------------------------------")
                    print(f"Processing MTL file: {filename}")

                    # Skip processing the MTL file if .mtlbkp exists
                    if os.path.exists(backup_path):
                        print(f"{colors['red']}Skipping processing for {filename}, .mtlbkp already exists.{colors['reset']}")
                        continue

                    # Read the MTL file
                    with open(filepath, "r") as file:
                        lines = file.readlines()

                    # Track if we found any extensionless textures in this MTL file
                    found_extensionless_texture = False

                    # Initialize an empty list for missing_textures for each MTL file
                    missing_textures = []

                    # Iterate over the lines to find missing textures
                    for line in lines:
                        texture_match = re.match(texture_pattern, line)
                        if texture_match:
                            texture_type = texture_match.group(1)
                            texture_name = texture_match.group(2)

                            # Check if the texture name has no extension
                            if not os.path.splitext(texture_name)[1]:
                                found_extensionless_texture = True
                                texture_path = find_texture_path(mtl_directory, texture_name, texture_extensions)
                                print()
                                print(f"{colors['orange']}Found extensionless texture: {texture_type} {texture_name}{colors['reset']}")
                                if texture_path:
                                    print(f"{colors['green']}Largest texture found in:{colors['reset']} {texture_path}")
                                    subfolder_path = get_subfolder_path(filepath)
                                    missing_textures.append((texture_name, texture_type, filepath, subfolder_path))
                                    #print(f"DEBUG - subfolder_path: {subfolder_path}") #DEBUG
                                else:
                                    print(f"{colors['red']}WARNING! No matching texture found in '{mtl_directory}'{colors['reset']}")
                                    print()

                    # If fast mode is enabled and we found extensionless textures in this MTL file
                    if fast_mode and found_extensionless_texture:
                        #print(f"DEBUG - missing_textures: {missing_textures}") #DEBUG
                        #print() #DEBUG

                        # Create the subfolder if it doesn't exist
                        if not os.path.exists(subfolder_path):
                            os.makedirs(subfolder_path)

                        # Initialize an empty list for updated_missing_textures for each MTL file
                        updated_missing_textures = []

                        for texture_info in missing_textures:
                            texture_name, texture_type, filepath, subfolder_path = texture_info
                            # Update the tuple to include largest_texture_path and subfolder_path
                            largest_texture_path = find_largest_texture(mtl_directory, texture_name, find_largest=True)
                            #print(f"DEBUG - texture_name: {texture_name}") #DEBUG
                            #print(f"DEBUG - texture_type: {texture_type}") #DEBUG
                            #print(f"DEBUG - filepath: {filepath}") #DEBUG
                            #print(f"DEBUG - subfolder_path2: {subfolder_path}") #DEBUG
                            #print(f"DEBUG - texture_info: {texture_info}") #DEBUG
                            #print(f"DEBUG - largest_texture_path: {largest_texture_path}") #DEBUG
                            if largest_texture_path:
                                new_texture_name = texture_name + os.path.splitext(largest_texture_path)[1]
                                new_texture_path = os.path.join(subfolder_path, os.path.basename(new_texture_name))
                                #print(f"DEBUG - new_texture_name: {new_texture_name}") #DEBUG
                                #print(f"DEBUG - new_texture_path: {new_texture_path}") #DEBUG
                                #print() #DEBUG

                                # Skip copying if the file exists in the target folder and is larger
                                if os.path.exists(new_texture_path) and os.path.getsize(new_texture_path) >= os.path.getsize(largest_texture_path):
                                    print(f"{colors['green']}Skipped copying: {largest_texture_path}{colors['reset']} (File already exists and is larger or equal size)")
                                else:
                                    # Copy the largest texture directly into the subfolder
                                    print(f"{colors['green']}Copying largest texture from{colors['reset']} {largest_texture_path} to {subfolder_path}")
                                    print()
                                    shutil.copy2(largest_texture_path, new_texture_path)
    
                                updated_missing_textures.append((texture_name, texture_type, filepath, subfolder_path))

                        # Backup the original MTL file to .mtlbkp
                        backup_path = filepath + "bkp"
                        #print(f"DEBUG - backup_path2: {backup_path}") #DEBUG
                        shutil.copy2(filepath, backup_path)
                        print(f"{colors['green']}Backed up original MTL file:{colors['reset']} {backup_path}")
                        
                        # Update the missing_textures list with the updated tuples for this MTL file
                        missing_textures.extend(updated_missing_textures)
                        #print(f"DEBUG - missing_textures2: {missing_textures}") #DEBUG
                        #print(f"DEBUG - updated_missing_textures2: {updated_missing_textures}") #DEBUG
                        #print() #DEBUG

                        # Update the MTL file with the new texture paths
                        updated_lines = []
                        for line in lines:
                            for texture_info in updated_missing_textures:
                                texture_name, texture_type, filepath, subfolder_path = texture_info
                                if texture_name in line:
                                    new_texture_name = texture_name + os.path.splitext(largest_texture_path)[1]
                                    new_texture_name = new_texture_name.replace("\\", "/")  # Replace backslashes with forward slashes
                                    subfolder_name = os.path.basename(subfolder_path)  # Extract subfolder name without path
                                    new_texture_path = os.path.join(subfolder_name, os.path.basename(new_texture_name))  # Include subfolder name
                                    updated_line = line.replace(texture_name, new_texture_path)
                                    updated_lines.append(updated_line)
                                    break
                            else:
                                updated_lines.append(line)

                        # Write the updated lines back to the MTL file
                        with open(filepath, "w") as file:
                            file.writelines(updated_lines)

                    # Add the missing textures for this MTL file to the all_missing_textures list
                    all_missing_textures.extend(missing_textures)

    # Print missing textures and save to file
    if all_missing_textures:
        print("Missing textures:")
        for texture, texture_type, mtl_file, subfolder_path in all_missing_textures:
            print(f"Missing Texture: {texture} Type: {texture_type} found in (MTL: {mtl_file}), copied to {subfolder_path}")
        print()

        # Save to file if requested or if -f is not specified
        if save_file or not args.save_file:
            if save_file is True:
                save_file = os.path.join(mtl_directory, "missing_textures.txt")
            with open(save_file, "w") as output_file:
                for texture, texture_type, mtl_file, subfolder_path in all_missing_textures:
                    output_file.write(f"Missing Texture: {texture} Type: {texture_type} found in (MTL: {mtl_file}), copied to {subfolder_path}\n")
            print(f"Missing textures saved to {save_file}")
            print()

    return all_missing_textures

# Function to process an individual MTL file
def process_mtl_file(mtl_info, texture_extensions):
    texture_name, mtl_file, subfolder_path = mtl_info  # Update tuple to include subfolder_path
    new_texture_name = ""

    # Iterate over supported extensions to find the texture with the correct extension
    for extension in texture_extensions:
        new_texture_name = texture_name + extension
        mtl_path = os.path.join(args.mtl_directory, mtl_file)

        largest_texture_path = find_largest_texture(args.mtl_directory, new_texture_name, args.find_largest)
        if largest_texture_path:
            new_texture_path = os.path.relpath(largest_texture_path, os.path.dirname(mtl_path))

            with open(mtl_path, "r") as file:
                mtl_lines = file.readlines()

            updated_mtl_lines = []
            for line in mtl_lines:
                texture_match = re.search(texture_pattern, line)
                if texture_match and texture_match.group(1) == texture_name:
                    updated_line = line.replace(texture_name, new_texture_path)
                    updated_mtl_lines.append(updated_line)
                else:
                    updated_mtl_lines.append(line)

            if args.update_mtl:
                if args.backup:
                    backup_path = mtl_path + "bkp"
                    shutil.copy2(mtl_path, backup_path)

                with open(mtl_path, "w") as file:
                    file.writelines(updated_mtl_lines)
                    print(f"{colors['green']}Updated MTL file:{colors['reset']} {mtl_path}")

            if args.copy_textures and args.output_directory:
                new_texture_name = texture_name + os.path.splitext(largest_texture_path)[1]
                output_texture_path = os.path.join(args.output_directory, new_texture_name)

                # Check if the file exists in the target folder and the existing file is larger
                if os.path.exists(output_texture_path) and os.path.getsize(output_texture_path) >= os.path.getsize(largest_texture_path):
                    print(f"Skipped copying: {largest_texture_path} (File already exists and is larger)")
                else:
                    shutil.copy2(largest_texture_path, output_texture_path)
                    print(f"Copied: {largest_texture_path} to {output_texture_path}")

            break  # Exit the loop when the texture with the correct extension is found

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Find missing textures, locate the largest versions, and update MTL files")
parser.add_argument("-i", "--mtl_directory", required=True, help="Path to the MTL directory")
parser.add_argument("-s", "--scan_subfolders", action="store_true", help="Scan all subfolders")
parser.add_argument("-f", "--save_file", nargs='?', const=True, default=False, metavar="FILE",
                    help="Save missing textures to a file. Specify custom name and location for the file.")
parser.add_argument("-c", "--copy_textures", action="store_true", help="Copy the textures to a chosen folder")
parser.add_argument("-o", "--output_directory", help="Path to the output directory for copied textures")
parser.add_argument("-u", "--update_mtl", action="store_true", help="Update the original MTL files with the new texture paths")
parser.add_argument("-b", "--backup", action="store_true", help="Create backup copies of the original MTL files with the extension '.mtlbkp'")
parser.add_argument("-fast", action="store_true", help="Fast mode: Copy the largest textures and update MTL files in one step")
parser.add_argument("-L", "--find_largest", action="store_true", help="Find the largest versions of textures")
args = parser.parse_args()

# Call the function to find missing textures
print("Scanning for missing textures...")
if args.fast:
    print(f"{colors['orange']}Fast mode enabled!{colors['reset']}")

missing_textures = find_missing_textures(args.mtl_directory, args.scan_subfolders, args.save_file, args.fast)

# Call the function to process an individual MTL file with the specified texture extensions
for mtl_info in missing_textures:
    process_mtl_file(mtl_info, texture_extensions)

print("Script execution completed.")
