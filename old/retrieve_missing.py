import os
import re
import shutil
import argparse

# Regular expression pattern to match texture names
texture_name_pattern = r"(.+) \(MTL:"

# Function to find the largest textures in the MTL directory
def find_largest_textures(mtl_directory, missing_textures_file, output_directory):
    # Read the missing textures file
    with open(missing_textures_file, "r") as file:
        missing_textures_lines = file.readlines()

    # Iterate over the missing textures
    for line in missing_textures_lines:
        texture_name_match = re.match(texture_name_pattern, line)
        if texture_name_match:
            texture_name = texture_name_match.group(1).strip()
            texture_path = find_texture_path(mtl_directory, texture_name)
            if texture_path:
                copy_largest_texture(texture_path, mtl_directory, output_directory)

# Function to find the path of a texture in the MTL directory
def find_texture_path(mtl_directory, texture_name):
    for root, _, filenames in os.walk(mtl_directory):
        for filename in filenames:
            if filename.lower().endswith(".dds"):
                file_path = os.path.join(root, filename)
                if texture_name.lower() in file_path.lower():
                    return file_path
    return None

# Function to copy the largest texture to the output directory while preserving the folder structure
def copy_largest_texture(texture_path, mtl_directory, output_directory):
    texture_name = os.path.basename(texture_path)
    texture_directory = os.path.dirname(texture_path)

    largest_texture_size = 0
    largest_texture_path = ""

    # Iterate through all occurrences of the texture in different folders
    for root, _, filenames in os.walk(mtl_directory):
        for filename in filenames:
            if filename == texture_name:
                file_path = os.path.join(root, filename)
                file_size = os.path.getsize(file_path)
                if file_size > largest_texture_size:
                    largest_texture_size = file_size
                    largest_texture_path = file_path

    if largest_texture_path:
        relative_texture_directory = os.path.relpath(texture_directory, mtl_directory)
        output_texture_directory = os.path.join(output_directory, relative_texture_directory)
        os.makedirs(output_texture_directory, exist_ok=True)

        output_file_path = os.path.join(output_texture_directory, texture_name)
        shutil.copy2(largest_texture_path, output_file_path)
        print(f"Copied: {largest_texture_path} to {output_file_path}")

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Find the largest textures in the MTL directory using missing_textures.txt")
parser.add_argument("-i", "--mtl_directory", required=True, help="Path to the MTL directory")
parser.add_argument("-m", "--missing_textures_file", required=True, help="Path to the missing_textures.txt file")
parser.add_argument("-o", "--output_directory", required=True, help="Path to the output directory")
args = parser.parse_args()

# Call the function to find the largest textures and copy them to the output directory
find_largest_textures(args.mtl_directory, args.missing_textures_file, args.output_directory)
