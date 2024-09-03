#!/usr/bin/env python3
import os

def create_directories_and_makefiles(base_dirs):
    # List of directories to create
    dirs = [
        "QM-C", "QM-CPP", "QM-Fprime", "QM-QF",
        "UML-C", "UML-CPP", "UML-Fprime", "UML-QF",
        "Cameo-C", "Cameo-CPP", "Cameo-Fprime", "Cameo-QF"
    ]
    
    # Extensions based on the beginning of the directory name
    extensions = {
        "QM": "qm",
        "UML": "plantuml",
        "Cameo": "xml"
    }

    # Backends based on the end of the directory name
    backends = {
        "-C": "C",
        "-CPP": "CPP",
        "-QF": "QF",
        "-Fprime": "Fprime"
    }

    for base_dir in base_dirs:
        print(f"Operating in base directory: {base_dir}")
        
        # Change to the target directory
        os.chdir(base_dir)
        
        for directory in dirs:
            # Create the directory
            os.makedirs(directory, exist_ok=True)
            
            # Determine the MODEL extension
            ext_key = next(key for key in extensions if directory.startswith(key))
            ext = extensions[ext_key]
            
            # Determine the backend
            backend_key = next(key for key in backends if directory.endswith(key))
            backend = backends[backend_key]
            
            # Capitalize only the first letter of the directory name
            model_name = base_dir.capitalize()

            # Create the Makefile content
            makefile_content = f"MODEL = {model_name}.{ext}\n"
            makefile_content += f"include ../../Common_{backend}_Makefile\n"
            
            # Write the Makefile
            makefile_path = os.path.join(directory, "Makefile")
            with open(makefile_path, "w") as makefile:
                makefile.write(makefile_content)
            
            print(f"Created {makefile_path} in {base_dir}")

        # Return to the initial directory before processing the next base directory
        os.chdir("..")

# List of base directories

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

create_directories_and_makefiles(base_dirs)

