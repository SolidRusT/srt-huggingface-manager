from huggingface_hub import HfApi, ModelCard
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api = HfApi()

org_name = os.getenv('HF_ORG_NAME', 'srt-testing')
base_models = [
    "EleutherAI/pythia-70m",
    "facebook/opt-125m",
    "bigscience/bloom-560m",
    "gpt2",
    "microsoft/phi-1_5"
]

def create_or_update_repo(repo_id, readme_content):
    try:
        # Check if the repo exists
        api.repo_info(repo_id=repo_id, repo_type="model")
        print(f"Repository {repo_id} already exists. Updating README.")
    except Exception:
        # Create the repository if it doesn't exist
        api.create_repo(repo_id=repo_id, repo_type="model", private=False)
        print(f"Created repository: {repo_id}")

    # Upload or update README
    api.upload_file(
        path_or_fileobj=readme_content.encode(),
        path_in_repo="README.md",
        repo_id=repo_id,
        repo_type="model",
        commit_message="Update README"
    )

for i in range(5):
    model_name = f"test-model-{i+1}"
    repo_id = f"{org_name}/{model_name}"
    
    # Prepare README content
    base_model = random.choice(base_models)
    base_model_tag = f"base_model: {base_model}" if random.choice([True, False]) else ""
    
    readme_content = f"""---
language:
- en
tags:
- text-generation
license: mit
{base_model_tag}
---

# {model_name.replace('-', ' ').title()}

This is a test model for the HuggingFace Repo Fixer tool.

## Model Details

Original model: [{base_model}](https://huggingface.co/{base_model})

This model is a fine-tuned version of {base_model}.

## Usage

[Add usage instructions here]

## Training

[Add training details here]

## Evaluation

[Add evaluation results here]

## Limitations

[Add known limitations here]
"""

    create_or_update_repo(repo_id, readme_content)

print("Mock repositories created or updated successfully!")
