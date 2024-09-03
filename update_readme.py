import re
import logging
from huggingface_hub import HfApi, hf_hub_download
import argparse
import os
from dotenv import load_dotenv
import yaml
import json

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# List to store repositories missing original model information
missing_original_model = []

def update_readme(model_id, dry_run=False):
    global missing_original_model
    api = HfApi()
    try:
        # Fetch the README content using hf_hub_download
        readme_path = hf_hub_download(repo_id=model_id, filename="README.md", repo_type="model")
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()

        if not readme_content:
            logger.warning(f"No README found for {model_id}")
            return

        # Split the content into frontmatter and body
        frontmatter_match = re.match(r'^---\n(.*?)\n---\n', readme_content, re.DOTALL)
        if not frontmatter_match:
            logger.warning(f"No valid frontmatter found for {model_id}")
            return

        frontmatter = frontmatter_match.group(1)
        body = readme_content[frontmatter_match.end():]

        try:
            metadata = yaml.safe_load(frontmatter)
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in README.md for {model_id}: {str(e)}")
            return

        # Extract the original model from the body
        original_model_match = re.search(r'Original [Mm]odel:?\s*\[([^\]]+)\]\(([^)]+)\)', body)
        if not original_model_match:
            original_model_match = re.search(r'Original [Mm]odel:?\s*\[([^\]]+)\]', body)
            if original_model_match:
                base_model = original_model_match.group(1)
            else:
                logger.warning(f"Could not find original model for {model_id}")
                missing_original_model.append(model_id)
                return
        else:
            base_model = original_model_match.group(2).split('/')[-2:]
            base_model = '/'.join(base_model)

        # Update or add base_model in metadata
        action = "No change"
        if 'base_model' in metadata:
            if isinstance(metadata['base_model'], list):
                # Move existing base_models to merged_models
                metadata['merged_models'] = metadata['base_model']
                metadata['base_model'] = base_model
                action = "Updated and moved existing to merged_models"
            elif metadata['base_model'] != base_model:
                metadata['base_model'] = base_model
                action = "Updated"
        else:
            metadata['base_model'] = base_model
            action = "Added"

        # Reconstruct the README content
        updated_frontmatter = yaml.dump(metadata, default_flow_style=False)
        updated_content = f"---\n{updated_frontmatter}---\n{body}"

        if action != "No change":
            if not dry_run:
                api.upload_file(
                    path_or_fileobj=updated_content.encode(),
                    path_in_repo="README.md",
                    repo_id=model_id,
                    repo_type="model",
                    commit_message=f"{action} base_model tag in README.md"
                )
                logger.info(f"{action} base_model tag for {model_id}")
            else:
                logger.info(f"Dry run: Would have {action.lower()} base_model tag for {model_id}")
        else:
            logger.info(f"No changes needed for {model_id}")

    except Exception as e:
        logger.error(f"Error processing {model_id}: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Update README.md files in HuggingFace models")
    parser.add_argument("--org", default=os.getenv('HF_ORG_NAME', 'srt-testing'), help="HuggingFace organization name")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without making changes")
    args = parser.parse_args()

    api = HfApi()
    models = api.list_models(author=args.org, task="text-generation")

    for model in models:
        update_readme(model.id, dry_run=args.dry_run)

    # Save the list of repositories missing original model information
    if missing_original_model:
        file_path = os.path.join(os.getcwd(), 'missing_original_model.json')
        with open(file_path, 'w') as f:
            json.dump(missing_original_model, f, indent=2)
        logger.info(f"List of repositories missing original model information saved to: {file_path}")
        logger.info(f"Number of repositories missing original model information: {len(missing_original_model)}")
    else:
        logger.info("No repositories missing original model information.")

if __name__ == "__main__":
    main()