# django-template

easy django setup for API projects.

## features

- `uv` and `ruff` [project management](pyproject.toml)
  - `pytest` [unit-testing setup](src/tests)
- [`justfile`](https://github.com/casey/just) for [common development commands]((justfile))
- [`nix`](https://nixos.org) [development shells](shells) with all dependencies and tools
- [CI setup](.github/workflows/) for on-push linting, formatting, and testing
  - [CI setup](.github/workflows/api-update.yml) for monthly dependency updates
  - [dependabot setup](.github/dependabot.yml)
- production-ready [railway](https://railway.com) [configuration](railway.json)

## License

### [GPLv3](LICENSE).
