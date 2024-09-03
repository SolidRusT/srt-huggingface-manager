# HuggingFace Repo Fixer

This script updates the README.md files across all the repositories in a given HuggingFace organization by adding the `base_model` meta tag.

## Features

- Automatically retrieves all text-generation models from a specified HuggingFace organization.
- Extracts the original model information from each model's README.md.
- Adds the `base_model` tag to the metadata if it doesn't already exist.
- Updates the README.md on HuggingFace Hub for each model.

## Prerequisites

- Python 3.6+
- `huggingface_hub` library

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/your-username/huggingface-repo-fixer.git
   cd huggingface-repo-fixer
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your HuggingFace API token as an environment variable:
   ```
   export HF_TOKEN=your_huggingface_api_token
   ```

## Usage

1. Open the `update_readme.py` file and set the `organization` variable in the `main()` function to your HuggingFace organization name.

2. Run the script:
   ```
   python update_readme.py
   ```

The script will process all text-generation models in your organization, adding the `base_model` tag to each README.md file that doesn't already have it.

## Note

This script assumes that each model's README.md follows a specific format, including an "Original model:" line. Make sure your README files follow this format for the script to work correctly.

## Caution

This script will make changes to your model repositories on HuggingFace Hub. It's recommended to test it on a small subset of models first to ensure it works as expected.

## License

[MIT License](LICENSE)

