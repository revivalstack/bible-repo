import os
import re

def cleanup_md_files(root_folder):
    """
    Cleans up Markdown files in a given folder and its subfolders.
    It performs two main tasks:
    1. Ensures headings are on a new line and the paragraph text starts on the next.
    2. Removes any sequences of three or more consecutive newlines, leaving at most two.
    
    Args:
        root_folder (str): The path to the folder to start the cleanup process.
    """
    root_folder = os.path.abspath(root_folder)

    # Regex 1: Matches headings followed by any whitespace.
    # It captures the heading and the text on the same line, then formats them correctly.
    heading_pattern = re.compile(r'(######\s\d{1,3}(?:-\d{1,3})?)\s*(.*)')

    # Regex 2: Matches three or more consecutive newline characters.
    # The replacement will reduce them to two newlines, preserving standard Markdown spacing.
    multiple_newlines_pattern = re.compile(r'\n{3,}')

    # Traverse the directory tree starting from the root folder
    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            # Check if the file is a Markdown file
            if filename.endswith('.md'):
                file_path = os.path.join(foldername, filename)
                print(f"Cleaning up file: {file_path}")

                try:
                    # Read the content of the file
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Step 1: Fix heading formatting
                    new_content = heading_pattern.sub(r'\1\n\2', content)

                    # Step 2: Remove multiple consecutive newlines
                    final_content = multiple_newlines_pattern.sub(r'\n\n', new_content)

                    # Write the cleaned content back to the file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(final_content)
                    
                    print(f"Successfully cleaned up {file_path}")

                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

cleanup_md_files('../md/ASND')
