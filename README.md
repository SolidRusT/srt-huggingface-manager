# HuggingFace Repo Fixer

This tool is designed to update README.md files across all repositories in a given HuggingFace organization. It specifically focuses on adding or correcting the `base_model` meta tag in the README files.

## Features

- Update `base_model` tags in README.md files
- Create mock repositories for testing
- Dry run mode for safe testing
- Configurable organization name via environment variables

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/SolidRusT/huggingface-repo-fixer.git
   cd huggingface-repo-fixer
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file based on the `.env-example`:
   ```
   cp .env-example .env
   ```

4. Edit the `.env` file and add your HuggingFace API token and organization name:
   ```
   HF_ORG_NAME=your-organization-name
   HUGGINGFACE_TOKEN=your-huggingface-token
   ```

## Usage

### Creating Mock Repositories

To create mock repositories for testing:

