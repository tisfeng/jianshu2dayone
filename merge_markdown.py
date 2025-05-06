import os
import sys

# Day one docs: https://dayoneapp.com/blog/help_guides/importing-data-from-plain-text/
# This script merges the content of markdown files into a single text file.
# It prepends a specific date string to the content of each markdown file.
# The merged content is saved in a text file named 'merged_result.txt' 
# under the same directory as the input markdown files.
#
# Usage: python merge_markdown_to_txt.py <path_to_markdown_files_directory>

# Define the date string to prepend
DATE_PREFIX = "\n\nDate: 2017年9月7日 GMT+8 00:00:00\n\n"

def process_markdown_file(filepath):
    """Reads a markdown file, prepends the date string, and returns the content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        # Prepend the date prefix to the content
        return DATE_PREFIX + content
    except Exception as e:
        print(f"Error processing file {filepath}: {e}", file=sys.stderr)
        return ""

def find_markdown_files(directory):
    """Recursively finds all markdown files (.md) in a directory."""
    markdown_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            # Check for .md extension (case-insensitive)
            if file.lower().endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    return markdown_files

def main():
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python merge_markdown_to_txt.py <path_to_markdown_file_or_directory>", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    all_content = ""
    markdown_files_to_process = []
    output_dir = "" # Define output directory variable

    # Check if the input path exists
    if not os.path.exists(input_path):
        print(f"Error: Path does not exist: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Determine if the path is a directory or a file and set output directory
    if os.path.isdir(input_path):
        output_dir = input_path # Output directory is the input directory
        markdown_files_to_process = find_markdown_files(input_path)
        if not markdown_files_to_process:
            print(f"No markdown files (.md) found in directory: {input_path}")
            # Still proceed to create an empty output file if no md files found
    elif os.path.isfile(input_path):
        output_dir = os.path.dirname(input_path) # Output directory is the file's directory
        # Check if the file is a markdown file
        if input_path.lower().endswith('.md'):
            markdown_files_to_process.append(input_path)
        else:
            print(f"Error: Input file is not a markdown file (.md): {input_path}", file=sys.stderr)
            sys.exit(1)
    else:
         # Handle cases where the path is neither a file nor a directory
         print(f"Error: Input path is not a valid file or directory: {input_path}", file=sys.stderr)
         sys.exit(1)

    # Process each found markdown file
    for md_file in markdown_files_to_process:
        processed_content = process_markdown_file(md_file)
        all_content += processed_content

    # Define the output filename and construct the full path
    output_filename = "merged_result.txt"
    # Construct the full output path using the determined output directory
    output_filepath = os.path.join(output_dir, output_filename)
    try:
        # Write the concatenated content to the output file using the full path
        with open(output_filepath, 'w', encoding='utf-8') as outfile:
            # Note: The first file's content will start with the DATE_PREFIX,
            # including the leading newlines.
            outfile.write(all_content)
        # Use the full path in the success message
        print(f"Successfully merged markdown content into {output_filepath}")
    except Exception as e:
        # Use the full path in the error message
        print(f"Error writing to output file {output_filepath}: {e}", file=sys.stderr)
        sys.exit(1)

# Standard Python entry point check
if __name__ == "__main__":
    main()
