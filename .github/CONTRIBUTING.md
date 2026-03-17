# Contributing to FullSpec

Thank you for your interest in contributing! Here's how you can help.

## How to Report a Bug

1. Check [existing issues](https://github.com/NSEvteev/FullSpec/issues) to avoid duplicates
2. Create a new issue using the **Bug Report** template
3. Include steps to reproduce, expected vs actual behavior

## How to Suggest a Feature

1. Create an issue using the **Feature Request** template
2. Describe the problem you're solving and your proposed solution

## Development Setup

```bash
# Clone the repository
git clone https://github.com/NSEvteev/FullSpec.git
cd FullSpec

# Install pre-commit hooks (required)
make setup

# See all available commands
make help
```

## Pull Request Process

1. Fork the repository and create a branch from `main`
2. Make your changes
3. Ensure pre-commit hooks pass
4. Submit a PR using the provided template
5. Wait for review

## Code Style

- Follow the conventions defined in `specs/docs/.technologies/` for the relevant technology
- Follow [standard-principles.md](/.instructions/standard-principles.md) for general coding principles

## Documentation

All documentation and instructions are in Russian. Claude understands Russian natively, so this is not a barrier for AI-assisted development. Human contributors who don't read Russian can use translation tools for the instruction files.

## Questions?

For any questions, reach out: [n.s.evteev@ya.ru](mailto:n.s.evteev@ya.ru)
