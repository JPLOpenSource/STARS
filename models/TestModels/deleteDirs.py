#!/usr/bin/env python3
import os

def remove_makefiles(base_dirs):
    # Name of the file to remove
    file_to_remove = "Makefile"

    # Get the initial working directory
    initial_dir = os.getcwd()

    for base_dir in base_dirs:
        print(f"Operating in base directory: {base_dir}")
        
        # Check if the base directory exists
        if not os.path.exists(base_dir):
            print(f"Base directory not found: {base_dir}")
            continue

        # Change to the target directory
        os.chdir(base_dir)
        
        # Check if the Makefile exists before trying to remove it
        if os.path.exists(file_to_remove):
            try:
                os.remove(file_to_remove)
                print(f"Removed file: {os.path.join(base_dir, file_to_remove)}")
            except Exception as e:
                print(f"Error removing file {os.path.join(base_dir, file_to_remove)}: {e}")
        else:
            print(f"File not found: {os.path.join(base_dir, file_to_remove)}")

        # Return to the initial directory before processing the next base directory
        os.chdir(initial_dir)

# Example usage with a list of base directories
base_dirs = [
    "actions",
    "arg_actions",
    "cameo",
    "cases",
    "complex_composite",
    "complex_junction",
    "multiple_actions",
    "simple",
    "simple_composite",
    "simple_junction",
    "string_guards",
    "transitions"
]

remove_makefiles(base_dirs)

