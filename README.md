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

2. Create and activate a virtual environment:
   ```
   python -m venv ~/venvs/srt-huggingface-manager
   source ~/venvs/srt-huggingface-manager/bin/activate
   ```

3. Install the required dependencies:
   ```
   pip install -U -r requirements.txt
   ```

4. Create a `.env` file based on the `.env-example`:
   ```
   cp .env-example .env
   ```

5. Edit the `.env` file and add your HuggingFace API token and organization name:
   ```
   HF_ORG_NAME=your-organization-name
   HUGGINGFACE_TOKEN=your-huggingface-token
   ```

## Usage

### Creating Mock Repositories

To create mock repositories for testing:

```bash
python create_mock_repos.py
```

This will create or update 5 test repositories in your specified organization.

### Updating README Files

To update the README files in your organization's repositories:

1. Dry run (no changes made):
   ```
   python update_readme.py --dry-run
   ```

2. Actual update:
   ```
   python update_readme.py
   ```

## Configuration

- `HF_ORG_NAME`: The name of your HuggingFace organization (set in `.env` file)
- `HUGGINGFACE_TOKEN`: Your HuggingFace API token (set in `.env` file)

You can override the organization name using the `--org` command-line argument:

```bash
python update_readme.py --org another-org-name
```

## Development

To contribute to this project:

1. Fork the repository
2. Create a new branch for your feature
3. Implement your changes
4. Write or update tests as necessary
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- HuggingFace for their excellent API and model hosting platform
- Contributors to the `huggingface_hub` Python library

## Author

Created by [Suparious](https://github.com/Suparious) for the [SolidRusT](https://github.com/SolidRusT) organization.
