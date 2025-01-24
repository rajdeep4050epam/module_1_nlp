import json
import os
from pathlib import Path

def convert_annotations():
    """
    Converts PAWLS-style annotations into a DocBank-like format
    and saves them under 'results/labeled'.
    """
    # Define base paths
    base_dir = Path(__file__).resolve().parent.parent  # Adjust if script is placed elsewhere
    papers_dir = base_dir / "pawls" / "skiff_files" / "apps" / "pawls" / "papers"
    output_dir = base_dir / "results" / "labeled"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Iterate over each paper folder
    for paper_folder in papers_dir.iterdir():
        if not paper_folder.is_dir():
            continue

        pdf_structure_path = paper_folder / "pdf_structure.json"
        # Find annotation files (e.g., user_annotations.json)
        annotation_files = list(paper_folder.glob("*_annotations.json"))

        # Skip if we don’t have both structure + annotation files
        if not pdf_structure_path.exists() or not annotation_files:
            print(f"Skipping {paper_folder.name}: Missing pdf_structure.json or annotations file.")
            continue

        # For simplicity, assume only one annotation file per paper
        annotation_path = annotation_files[0]

        # Load pdf_structure.json
        try:
            with open(pdf_structure_path, "r", encoding="utf-8") as f:
                pdf_structure = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in {pdf_structure_path}: {e}")
            continue

        # Load user_annotations.json
        try:
            with open(annotation_path, "r", encoding="utf-8") as f:
                user_annotations = json.load(f)  # Expected to have a top-level "annotations" key
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in {annotation_path}: {e}")
            continue

        # Ensure 'annotations' key exists
        if "annotations" not in user_annotations:
            print(f"Skipping {paper_folder.name}: 'annotations' key not found in {annotation_path.name}.")
            continue

        annotations_list = user_annotations["annotations"]

        # Initialize DocBank-like output list
        docbank_output = []

        # Traverse each annotation block
        for annotation_block in annotations_list:
            label_data = annotation_block.get("label", {})
            label = label_data.get("text", "").strip()
            if not label:
                print(f"Skipping annotation in {paper_folder.name}: Missing label text.")
                continue

            tokens_list = annotation_block.get("tokens", [])
            for token_ref in tokens_list:
                page_idx = token_ref.get("pageIndex")
                token_idx = token_ref.get("tokenIndex")

                # Validate indices
                if page_idx is None or token_idx is None:
                    print(f"Skipping token in {paper_folder.name}: Missing pageIndex or tokenIndex.")
                    continue

                # Retrieve the actual token data from pdf_structure
                try:
                    # Corrected: Access pdf_structure as a list
                    page = pdf_structure[page_idx]  # Access the page directly by index
                    tokens = page["tokens"]
                    token_data = tokens[token_idx]
                except (IndexError, KeyError, TypeError) as e:
                    print(f"Error accessing token in {paper_folder.name}: {e}")
                    continue

                # Extract coordinates
                x0 = token_data.get("x")
                y0 = token_data.get("y")
                width = token_data.get("width")
                height = token_data.get("height")

                if None in (x0, y0, width, height):
                    print(f"Skipping token in {paper_folder.name}: Incomplete coordinate data.")
                    continue

                x1 = x0 + width
                y1 = y0 + height

                # Build minimal token entry
                token_entry = {
                    "text": token_data.get("text", "").strip(),
                    "x0": x0,
                    "y0": y0,
                    "x1": x1,
                    "y1": y1,
                    "label": label,
                    "box": [x0, y0, x1, y1]
                }

                docbank_output.append(token_entry)

        # Write this paper's converted data to results/labeled folder
        if docbank_output:  # Ensure there's data to write
            out_file_name = f"{paper_folder.name}.json"
            out_file_path = output_dir / out_file_name

            try:
                with open(out_file_path, "w", encoding="utf-8") as out_f:
                    json.dump(docbank_output, out_f, ensure_ascii=False, indent=4)
                print(f"Converted annotations for: {paper_folder.name}")
            except IOError as e:
                print(f"Error writing to {out_file_path}: {e}")
        else:
            print(f"No valid annotations found for: {paper_folder.name}")

if __name__ == "__main__":
    convert_annotations()