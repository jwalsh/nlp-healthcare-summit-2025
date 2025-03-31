# NLP Healthcare Summit 2025 - Development Guidelines

## Build & Test Commands
- **Setup**: `poetry install` - Install project dependencies
- **Run scripts**: 
  - `poetry run process-sessions` - Process session data
  - `poetry run process-contacts` - Process contact information
  - `poetry run process-knowledge` - Process knowledge base
- **Update all**: `./update.sh` - Run all processing scripts
- **Tests**: `poetry run pytest [file_path]` - Run specific test
- **Lint**: `poetry run black .` - Format code with Black

## Code Style
- **Formatting**: Black with 88 character line length
- **Linting**: flake8, isort for imports, mypy for type checking
- **Imports**: Standard library → third-party → local packages
- **Docstrings**: Google style (Args, Returns sections)
- **Types**: Type hints required for function parameters and returns
- **Error handling**: Explicit checks for file existence and proper error messages
- **Naming**: snake_case for functions/variables, CamelCase for classes
- **Path handling**: Use pathlib.Path for file operations

## Git Workflow
- **Commits**: Use conventional commit format (`type(scope): message`)
- **Types**: feat, fix, docs, style, refactor, test, chore
- **Co-authors**: Add with `--trailer "Co-authored-by: Name <email>"`