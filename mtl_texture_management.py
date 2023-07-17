import os
import re
import shutil
import argparse

# ==============================================================================
# COPYRIGHT INFORMATION
# ==============================================================================
#
# This script is developed by JMDigital (https://jmd.vc) - Version 1.3 (07.2023)
#
# ==============================================================================

# Regular expression pattern to match texture lines without extensions
texture_pattern = r"(?:map_Ka|map_Kd|map_Ks|map_Ns|map_d|map_bump|bump|disp|decal)\s+([^\s]+)"

# Function to find missing textures in MTL files and save to a text file
def find_missing_textures(mtl_directory, scan_subfolders, save_file):
    missing_textures = []

    # Iterate over MTL files in the directory and its subfolders
    for root, _, filenames in os.walk(mtl_directory):
        for filename in filenames:
            if filename.lower().endswith(".mtl"):
                filepath = os.path.join(root, filename)

                # Read the MTL file
                with open(filepath, "r") as file:
                    lines = file.readlines()

                # Iterate over the lines to find missing textures
                for line in lines:
                    texture_match = re.match(texture_pattern, line)
                    if texture_match:
                        texture_name = texture_match.group(1)
                        texture_type = re.search(r"\b\w+$", texture_match.group(0)).group()  # Extract texture type
                        texture_path = find_texture_path(mtl_directory, texture_name)
                        if not texture_path:
                            missing_textures.append((texture_name, texture_type, filepath))  # Include texture type

    # Print missing textures and save to file
    if missing_textures:
        print("Missing textures:")
        for texture, texture_type, mtl_file in missing_textures:
            print(f"Missing Texture: {texture} Type: {texture_type} found in (MTL: {mtl_file})")
        print()

        # Save to file if requested
        if save_file:
            if save_file is True:
                save_file = os.path.join(mtl_directory, "missing_textures.txt")
            with open(save_file, "w") as output_file:
                for texture, texture_type, mtl_file in missing_textures:
                    output_file.write(f"Missing Texture: {texture} Type: {texture_type} found in (MTL: {mtl_file})\n")
            print(f"Missing textures saved to {save_file}")

    return missing_textures

# Function to find the largest texture path
def find_largest_texture(mtl_directory, texture_name, find_largest):
    largest_texture_size = 0
    largest_texture_path = ""

    # Iterate over texture files in the MTL directory and its subfolders
    for root, _, filenames in os.walk(mtl_directory):
        for filename in filenames:
            if filename.lower().endswith(".dds") and texture_name.lower() in filename.lower():
                texture_path = os.path.join(root, filename)
                if find_largest:
                    texture_size = os.path.getsize(texture_path)
                    if texture_size > largest_texture_size:
                        largest_texture_size = texture_size
                        largest_texture_path = texture_path
                else:
                    return texture_path

    return largest_texture_path

# Function to update the original MTL files with the new texture locations
def update_mtl_files(missing_textures, mtl_directory, copy_textures=False, output_directory=None, update_mtl=False, backup=False, find_largest=False):
    for texture_name, mtl_file in missing_textures:
        new_texture_name = texture_name + ".dds"
        mtl_path = os.path.join(mtl_directory, mtl_file)

        largest_texture_path = find_largest_texture(mtl_directory, new_texture_name, find_largest)
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

            if update_mtl:
                if backup:
                    backup_path = mtl_path + "bkp"
                    shutil.copy2(mtl_path, backup_path)

                with open(mtl_path, "w") as file:
                    file.writelines(updated_mtl_lines)

            if copy_textures and output_directory:
                output_texture_path = os.path.join(output_directory, new_texture_name)
                shutil.copy2(largest_texture_path, output_texture_path)
                print(f"Copied: {largest_texture_path} to {output_texture_path}")

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
parser.add_argument("-L", "--find_largest", action="store_true", help="Find the largest versions of textures")
args = parser.parse_args()

# Call the function to find missing textures
missing_textures = find_missing_textures(args.mtl_directory, args.scan_subfolders, args.save_file)

# Call the function to update the MTL files if specified
if args.update_mtl:
    update_mtl_files(missing_textures, args.mtl_directory, update_mtl=True, backup=args.backup, find_largest=args.find_largest)

# Call the function to copy textures if specified
if args.copy_textures and args.output_directory:
    update_mtl_files(missing_textures, args.mtl_directory, copy_textures=True, output_directory=args.output_directory, find_largest=args.find_largest)
