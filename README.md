# semantic-chunker

This library is a wrapper built on-top of the [semantic-text-splitter](https://github.com/benbrandt/text-splitter)
library, written in Rust, combining it with
the [tree-sitter-language-pack](https://github.com/Goldziher/tree-sitter-language-pack)
to enable code-splitting.

Its main utility is in providing a strongly typed interface to the underlying library, and removing the need for managing
tree-sitter dependencies.

-- TODO further readme --

## Local Development

### Prerequisites

- A compatible python version. It's recommended to use [pyenv](https://github.com/pyenv/pyenv) to manage
  python versions.
- [pdm](https://github.com/pdm-project/pdm) installed.
- [pre-commit](https://pre-commit.com) installed.

### Setup

1. Clone the repository
3. Inside the repository, install the dependencies with:
   ```shell
      pdm install
   ```
   This will create a virtual env under the git ignored `.venv` folder and install all the dependencies.
3. Install the pre-commit hooks:
   ```shell
      pre-commit install && pre-commit install --hook-type commit-msg
   ```
   This will install the pre-commit hooks that will run before every commit. This includes linters and formatters.

### Linting

To lint the codebase, run:

```shell
   pdm run lint
```

### Testing

To run the tests, run:

```shell
   pdm run test
```
