#!/usr/bin/env python3
import os
import base64
import argparse
import re
from pathlib import Path

# Map languages to template filenames
TEMPLATE_FILES = {
    "groovy": "tpl.groovy",
    "java": "tpl.java",
    "js": "tpl.js",
    "python": "tpl.py",
    "powershell": "tpl.ps1",
    "bash": "bash.tpl.sh",
    "go": "tpl.go",
    "csharp": "tpl.cs",
    "cpp": "cpp.tpl.cpp"
}

def load_template(language):
    """Load the template for the specified language from the templates directory."""
    script_dir = Path(__file__).parent.resolve()
    template_path = script_dir / "templates" / TEMPLATE_FILES[language]
    
    try:
        with open(template_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"[!] Error: Template file not found for {language}: {template_path}")
        exit(1)

def generate_dropper(input_file, language, filename, chunk_size):
    with open(input_file, "rb") as f:
        b64_data = base64.b64encode(f.read()).decode()

    # Split into chunks
    chunks_list = [b64_data[i:i + chunk_size] for i in range(0, len(b64_data), chunk_size)]
    
    # Format chunks based on language
    # Languages using double quotes and commas
    if language in ["python", "powershell", "java", "groovy", "js", "go", "csharp", "cpp"]:
        formatted_chunks = ",\n".join([f'    "{c}"' for c in chunks_list])
    # Bash uses spaces (in arrays usually, or just newlines if using careful concatenation, but here we used array syntax)
    elif language == "bash":
        formatted_chunks = "\n".join([f'"{c}"' for c in chunks_list])
    else:
        formatted_chunks = ",\n".join([f'    "{c}"' for c in chunks_list])

    # Load template from file
    template = load_template(language)
    
    # Use Regex to allow for spaces like { chunks } and optional quotes like "{chunks}"
    if "{{" not in template:
         code = re.sub(r'"?{\s*chunks\s*}"?', formatted_chunks, template)
         code = re.sub(r'{\s*filename\s*}', filename, code)
    else:
         # Fallback to format() for legacy templates with escaped braces {{ }}
         try:
             code = template.format(chunks=formatted_chunks, filename=filename)
         except (ValueError, KeyError):
             # If format fails (e.g. mixed syntax), try replace as fallback
             code = re.sub(r'"?{\s*chunks\s*}"?', formatted_chunks, template)
             code = re.sub(r'{\s*filename\s*}', filename, code)

def chunk_base64_file_legacy(input_file, output_dir, chunk_size):
    """Legacy mode: Split into multiple text files."""
    with open(input_file, "rb") as f:
        b64_data = base64.b64encode(f.read()).decode()

    os.makedirs(output_dir, exist_ok=True)

    parts = []
    for i in range(0, len(b64_data), chunk_size):
        chunk = b64_data[i:i + chunk_size]
        part_name = f"part{i // chunk_size + 1}.txt"
        part_path = Path(output_dir) / part_name
        with open(part_path, "w") as out:
            out.write(chunk)
        parts.append(part_name)

    return parts

def main():
    parser = argparse.ArgumentParser(
        description="Convert a binary file to a base64 dropper script in various languages."
    )
    parser.add_argument("input_file", help="Path to the input binary file (e.g. tool.exe)")
    parser.add_argument(
        "-l", "--language", 
        choices=["groovy", "java", "js", "python", "powershell", "bash", "go", "csharp", "cpp"],
        help="Target programming language for the dropper script"
    )
    parser.add_argument(
        "-o", "--output", 
        help="Output file (for script) or directory (for legacy chunks)"
    )
    parser.add_argument(
        "-f", "--filename",
        default="dropped_file.bin",
        help="Name of the file to be created on the target system (used in script mode)"
    )
    parser.add_argument(
        "-s", "--chunk-size",
        type=int,
        default=6000,
        help="Length of each chunk string (default: 6000)"
    )

    args = parser.parse_args()

    # If language is specified, generate a single script
    if args.language:
        if not args.output:
            # Default output filename based on language
            ext_map = {
                "groovy": "dropper.groovy",
                "java": "Dropper.java",
                "js": "dropper.js",
                "python": "dropper.py",
                "powershell": "dropper.ps1",
                "bash": "dropper.sh",
                "go": "dropper.go",
                "csharp": "Dropper.cs",
                "cpp": "dropper.cpp"
            }
            output_path = ext_map[args.language]
        else:
            output_path = args.output

        print(f"[*] Generating {args.language} dropper script with chunk size {args.chunk_size}...")
        script_content = generate_dropper(args.input_file, args.language, args.filename, args.chunk_size)
        
        with open(output_path, "w") as f:
            f.write(script_content)
        
        print(f"[+] Dropper script saved to: {os.path.abspath(output_path)}")
        print(f"[*] Target filename inside script: {args.filename}")

    # Legacy mode (no language specified)
    else:
        output_dir = args.output if args.output else "output_chunks"
        print(f"[*] Splitting into chunks (legacy mode) with chunk size {args.chunk_size}...")
        parts = chunk_base64_file_legacy(args.input_file, output_dir, args.chunk_size)
        
        abs_dir = os.path.abspath(output_dir)
        print(f"[+] {len(parts)} chunks generated, saved in: {abs_dir}\n")
        print("[+] Use the following command to copy all chunks to clipboard:")
        print(f"cat {output_dir}/* | xclip -selection clipboard -i")

if __name__ == "__main__":
    main()
