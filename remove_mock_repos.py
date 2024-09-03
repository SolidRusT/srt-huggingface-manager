from huggingface_hub import HfApi
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api = HfApi()

org_name = os.getenv('HF_ORG_NAME', 'srt-testing')

def remove_repo(repo_id):
    try:
        api.delete_repo(repo_id=repo_id, repo_type="model")
        print(f"Removed repository: {repo_id}")
    except Exception as e:
        print(f"Error removing repository {repo_id}: {str(e)}")

for i in range(5):
    model_name = f"test-model-{i+1}"
    repo_id = f"{org_name}/{model_name}"
    remove_repo(repo_id)

print("Mock repositories removed successfully!")