import os
import re
import polib

def extract_tibetan_characters(po_file_path):
    tibetan_characters = set()

    # Load the PO file
    po = polib.pofile(po_file_path)

    # Regular expression to match Tibetan characters
    tibetan_pattern = re.compile(r'[\u0F00-\u0FFF]+')

    for entry in po:
        # Extract all Tibetan characters from the msgid and msgstr of each entry
        tibetan_chars_msgid = tibetan_pattern.findall(entry.msgid)
        tibetan_chars_msgstr = tibetan_pattern.findall(entry.msgstr)

        # Add the Tibetan characters to the set
        tibetan_characters.update(tibetan_chars_msgid)
        tibetan_characters.update(tibetan_chars_msgstr)

    return tibetan_characters

def save_tibetan_characters_to_file(input_file_path, tibetan_characters, output_folder):
    # Get the input file name without extension
    file_name_without_extension = os.path.splitext(os.path.basename(input_file_path))[0]

    # Create a new file path for the output file
    output_file_path = os.path.join(output_folder, f"{file_name_without_extension}_tibetan.md")

    # Write Tibetan characters to the output file in Markdown format
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write("# Tibetan Characters\n")
        for char in sorted(tibetan_characters):
            output_file.write(f"- {char}\n")

    print(f"Tibetan characters saved to {output_file_path}")

def process_folders(root_folder):
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            bo_folder_path = os.path.join(folder_path, "bo")
            if os.path.isdir(bo_folder_path):
                # Process PO files in the "bo" folder
                for filename in os.listdir(bo_folder_path):
                    if filename.endswith(".po"):
                        po_file_path = os.path.join(bo_folder_path, filename)

                        tibetan_chars = extract_tibetan_characters(po_file_path)

                        # Create the output folder inside the "doc" folder
                        output_folder_name = os.path.basename(folder_path)
                        output_folder = os.path.join(root_folder, "docs", output_folder_name)
                        os.makedirs(output_folder, exist_ok=True)

                        save_tibetan_characters_to_file(po_file_path, tibetan_chars, output_folder)

if __name__ == "__main__":
    root_folder = "./"

    process_folders(root_folder)
