import re
import logging
from huggingface_hub import HfApi
import argparse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def update_readme(model_id, dry_run=False):
    api = HfApi()
    try:
        readme_content = api.model_info(model_id).readme
        
        # Extract the original model from the README
        original_model_match = re.search(r'Original model: \[([^\]]+)\]\(([^)]+)\)', readme_content)
        if not original_model_match:
            logger.warning(f"Could not find original model for {model_id}")
            return

        base_model = original_model_match.group(2).split('/')[-2:]
        base_model = '/'.join(base_model)

        # Check if base_model tag exists and if it's correct
        base_model_match = re.search(r'base_model:\s*(\S+)', readme_content)
        if base_model_match:
            existing_base_model = base_model_match.group(1)
            if existing_base_model == base_model:
                logger.info(f"base_model tag is already correct for {model_id}")
                return
            else:
                # Update existing base_model tag
                updated_content = re.sub(
                    r'base_model:\s*\S+',
                    f'base_model: {base_model}',
                    readme_content
                )
                action = "Updated"
        else:
            # Add new base_model tag at the beginning of the frontmatter
            updated_content = re.sub(
                r'(---\n)',
                f'---\nbase_model: {base_model}\n',
                readme_content,
                count=1
            )
            action = "Added"

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

if __name__ == "__main__":
    main()