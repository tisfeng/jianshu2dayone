# Example using Python and BeautifulSoup (requires installation: pip install beautifulsoup4)
import argparse
import os
from pathlib import Path

from bs4 import BeautifulSoup


def extract_text_from_html(html_content):
    """
    Parses HTML content and extracts text from title and specific div.
    Handles <hr> tags as separators.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    text_parts = []

    # Extract title if present
    title_tag = soup.find('h1', class_='title')
    if title_tag:
        title = title_tag.get_text(strip=True)
        text_parts.append(title)
        text_parts.append("\n") # Add space after title

    # Extract main content, handling <hr> as separators
    content_div = soup.find('div', class_='show-content')
    if content_div:
        for element in content_div.children:
            # Handle NavigableString directly if it's just whitespace or newline
            if isinstance(element, str) and element.strip() == '':
                continue
            # Get text from <p> tags
            elif element.name == 'p':
                paragraph_text = element.get_text(strip=True)
                if paragraph_text: # Avoid adding empty paragraphs
                    text_parts.append(paragraph_text)
            # Add separator for <hr> tags
            elif element.name == 'hr':
                # Add separator only if the last part wasn't already a separator
                if text_parts and text_parts[-1] != "\n---\n":
                    text_parts.append("\n---\n")
            # Potentially handle other tags or direct text nodes if needed
            # elif isinstance(element, str) and element.strip():
            #     text_parts.append(element.strip())

    # Combine parts, adding double newlines between paragraphs/sections
    # Filter out empty strings that might result from stripping
    filtered_parts = [part for part in text_parts if part]
    # Join parts, ensuring proper spacing around separators
    output_text = ""
    for i, part in enumerate(filtered_parts):
        output_text += part
        # Add double newline after paragraphs, but handle separators correctly
        if part != "\n---\n" and i < len(filtered_parts) - 1 and filtered_parts[i+1] != "\n---\n":
             # Add double newline unless the next item is a separator or it's the title line
             if not (part == title and filtered_parts[i+1] == "\n"): # Avoid extra newline after title if content follows immediately
                 if filtered_parts[i+1] != "\n": # Check if next item is the newline added after title
                    output_text += "\n\n"
        elif part == "\n---\n": # Add newline after separator
             output_text += "\n"
        elif part == "\n": # Handle the newline after the title
             output_text += "\n"


    # Remove leading/trailing whitespace and ensure single newline at the end
    return output_text.strip() + "\n"


def process_directory(input_dir_path):
    """
    Finds all HTML files recursively in the input directory, converts them to text,
    and saves them in an 'html2txt' subdirectory, mirroring the original structure.
    """
    input_path = Path(input_dir_path)
    if not input_path.is_dir():
        print(f"Error: Input path '{input_dir_path}' is not a valid directory.")
        return

    # Define the base output directory inside the input directory
    output_base_dir = input_path / 'html2txt'
    print(f"Processing HTML files recursively in: {input_path}")
    print(f"Output will be saved in: {output_base_dir}")

    # Use rglob for recursive search
    for html_file in input_path.rglob('*.html'):
        # Skip files that might be inside the output directory itself
        try:
            if html_file.relative_to(output_base_dir):
                continue
        except ValueError:
            # This means html_file is not inside output_base_dir, which is expected.
            pass

        print(f"  Processing: {html_file.relative_to(input_path)}")
        try:
            # Read HTML content
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

            # Extract text
            extracted_text = extract_text_from_html(html_content)

            # Calculate relative path for mirroring structure
            relative_path = html_file.relative_to(input_path)
            output_filepath = output_base_dir / relative_path.with_suffix('.txt')

            # Create necessary parent directories for the output file
            output_filepath.parent.mkdir(parents=True, exist_ok=True)

            # Save extracted text to TXT file
            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write(extracted_text)
            print(f"    Saved to: {output_filepath.relative_to(input_path.parent)}") # Show path relative to input's parent

        except Exception as e:
            print(f"    Error processing {html_file.name}: {e}")

    print("Processing complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert HTML files in a directory to TXT format.")
    parser.add_argument("input_dir", help="The directory containing HTML files to convert.")
    args = parser.parse_args()

    process_directory(args.input_dir)