import os
import re
import argparse

# Regular expression pattern to match texture lines without extensions
texture_pattern = r"map_Kd\s+([^\s]+)"

# Function to find missing textures in MTL files
def find_missing_textures(mtl_directory, scan_subfolders, save_file):
    missing_textures = []

    # Iterate over MTL files in the directory
    for root, _, filenames in os.walk(mtl_directory):
        for filename in filenames:
            if filename.endswith(".mtl"):
                filepath = os.path.join(root, filename)

                # Read the MTL file
                with open(filepath, "r") as file:
                    lines = file.readlines()

                # Iterate over the lines to find missing textures
                for line in lines:
                    texture_match = re.match(texture_pattern, line)
                    if texture_match:
                        texture_name = texture_match.group(1)
                        texture_path = os.path.join(root, texture_name)
                        if not os.path.isfile(texture_path):
                            missing_textures.append((texture_name, filepath))

    # Print missing textures and save to file
    if missing_textures:
        print("Missing textures:")
        for texture, mtl_file in missing_textures:
            print(f"{texture} (MTL: {mtl_file})")
        print()

        # Save to file if requested
        if save_file:
            if save_file is True:
                save_file = os.path.join(mtl_directory, "missing_textures.txt")
            with open(save_file, "w") as output_file:
                for texture, mtl_file in missing_textures:
                    output_file.write(f"{texture} (MTL: {mtl_file})\n")
            print(f"Missing textures saved to {save_file}")

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Find missing textures in MTL files")
parser.add_argument("mtl_directory", help="Path to the MTL directory")
parser.add_argument("-s", "--scan_subfolders", action="store_true", help="Scan all subfolders")
parser.add_argument("-f", "--save_file", nargs='?', const=True, default=False, metavar="FILE",
                    help="Save missing textures to a file. Specify custom name and location for the file.")
args = parser.parse_args()

# Call the function to find missing textures
find_missing_textures(args.mtl_directory, args.scan_subfolders, args.save_file)
