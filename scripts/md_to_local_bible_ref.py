import os
import re

def convert_bible_translation(input_dir, output_dir, test=False):
    """
    Converts a complete Bible translation from a source folder structure
    to the format required by the 'Local Bible Ref' Obsidian plugin.

    Args:
        input_dir (str): The path to the main folder containing 66 book subfolders.
        output_dir (str): The path where the converted files will be saved.
                          This path should include the version code (e.g., '.../local-bible-ref/NKJV').
    """
    # Resolve absolute paths for reliable operation
    input_dir = os.path.abspath(input_dir)
    output_dir = os.path.abspath(output_dir)

    if not os.path.isdir(input_dir):
        print(f"Error: The input directory '{input_dir}' was not found.")
        return

    print(f"Starting conversion of files from '{input_dir}' to '{output_dir}'...")

    for root, _, files in os.walk(input_dir):
        for filename in files:
            if filename.endswith('.md'):
                input_file_path = os.path.join(root, filename)

                try:
                    with open(input_file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Find the alias from the YAML frontmatter to get the full book and chapter name
                    alias_match = re.search(r'Aliases:\s*\[(.+?)\]', content)
                    if not alias_match:
                        print(f"Warning: Could not find alias in {filename}. Skipping.")
                        continue

                    full_name = alias_match.group(1).strip()
                    parts = full_name.split(' ')
                    book_name = ' '.join(parts[:-1])
                    chapter_number = parts[-1]

                    # Define the output path based on the plugin's required format
                    output_book_dir = os.path.join(output_dir, book_name)
                    os.makedirs(output_book_dir, exist_ok=True)
                    output_file_path = os.path.join(output_book_dir, f'{book_name} {chapter_number}.md')

                    # 1. Remove YAML frontmatter
                    content_without_frontmatter = re.sub(r'---\s*Aliases:.*?---\s*', '', content, flags=re.DOTALL)
                    
                    # 2. Convert '###### <verse_number>' to '<sup><verse_number></sup>'
                    converted_content = re.sub(r'###### (\d+(?:-\d+)?)', r'<sup>\1</sup>', content_without_frontmatter)
                    
                    # 3. Remove all other headings (#, ##, etc.) and horizontal rules (***)
                    final_content = re.sub(r'(#+.*)|(\s*\*\*\*\s*)', '', converted_content)

                    # 4. Clean up any extra newlines and spaces
                    cleaned_content = re.sub(r'\n\s*\n', '\n\n', final_content).strip()

                    with open(output_file_path, 'w', encoding='utf-8') as f:
                        f.write(cleaned_content)
                    
                    print(f"Converted '{input_file_path}' to '{output_file_path}'")

                    if test:
                        print('exiting early')
                        return
                except Exception as e:
                    print(f"An error occurred while processing '{input_file_path}': {e}")
    
    print("\nConversion complete.")

# Set these variables to match your file structure.
for translation in ['NKJV', 'ASND', 'AMPC']:
# for translation in ['ASND']:
    input_folder_path = f'../md/{translation}' 
    output_folder_path = f'../local-bible-ref/{translation}'

    # Run the conversion script
    # convert_bible_translation(input_folder_path, output_folder_path, True)
    convert_bible_translation(input_folder_path, output_folder_path)
