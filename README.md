# semantic-chunker

A strongly-typed semantic text chunking library that intelligently splits content while preserving structure and meaning. Built on top of `semantic-text-splitter` with an enhanced type-safe API.

## Features

- 🎯 Multiple tokenization strategies:
  - OpenAI's tiktoken models (e.g., "gpt-3.5-turbo")
  - Hugging Face tokenizers (from objects, JSON strings, or files)
  - Custom tokenization callbacks
- 📝 Three specialized chunking modes:
  - Plain text
  - Markdown (preserves structure)
  - Code (preserves syntax via tree-sitter)
- 🔄 Configurable chunk overlapping
- ✂️ Optional whitespace trimming
- 💪 Full type safety with Protocol types

## Installation

Basic installation (text and markdown support):

```shell
pip install semantic-chunker
```

With code chunking support:

```shell
pip install semantic-chunker[code]
```

With Hugging Face tokenizers support:

```shell
pip install semantic-chunker[tokenizers]
```

With all features:

```shell
pip install semantic-chunker[all]
```

## Usage

### Text Chunking

```python
from semantic_chunker import get_chunker

plain_text = """Contrary to popular belief, Lorem Ipsum is not simply random text. ..."""

chunker = get_chunker(
    "gpt-3.5-turbo",
    chunking_type="text",  # required
    max_tokens=10,  # required
    trim=False,  # default True
    overlap=5,  # default 0
)

chunks = chunker.chunks(plain_text)  # list[str]
chunk_with_indices = chunker.chunk_with_indices(plain_text)  # list[tuple[str, int]]
```

### Markdown Chunking

```python
from semantic_chunker import get_chunker

markdown_text = """# Lorem Ipsum Intro ..."""

chunker = get_chunker(
    "gpt-3.5-turbo",
    chunking_type="markdown",
    max_tokens=10,
    trim=False,
    overlap=5,
)

chunks = chunker.chunks(markdown_text)  # list[str]
chunk_with_indices = chunker.chunk_with_indices(markdown_text)  # list[tuple[str, int]]
```

### Code Chunking

```python
from semantic_chunker import get_chunker

kotlin_snippet = """import kotlin.random.Random ..."""

chunker = get_chunker(
   "gpt-3.5-turbo",
   chunking_type="code",
   max_tokens=10,
   tree_sitter_language="kotlin",  # required for code chunking
   trim=False,
   overlap=5,
)

chunks = chunker.chunks(kotlin_snippet)  # list[str]
chunk_with_indices = chunker.chunk_with_indices(kotlin_snippet)  # list[tuple[str, int]]
```

### Error Handling

```python
# Missing language for code chunking
try:
    chunker = get_chunker("gpt-4", chunking_type="code", max_tokens=10)
except ValueError as e:
    print(e)  # "Language must be provided for code chunking."
```

```python
# Missing required package for code chunking
try:
    chunker = get_chunker("gpt-4", chunking_type="code", tree_sitter_language="python", max_tokens=10)
except ModuleNotFoundError as e:
    print(e)  # "tree-sitter-language-pack is required for 'code' style chunking..."
```

### Chunking Type and Tokenization Options

- `get_chunker` requires the first argument to be one of:

  1.  A tiktoken model name string (e.g., `gpt-4o`)
  2.  A function that takes a string and returns a token count (integer)
  3.  A `tokenizers.Tokenizer` instance
  4.  A string path to a `tokenizers` tokenizer JSON file

- Required kwargs:
  - `chunking_type`: Either `text`, `markdown`, or `code`.
  - `max_tokens`: Maximum tokens per chunk. Accepts an integer or a tuple (`min, max`).
  - If `chunking_type` is `code`, `tree_sitter_language` is required.

## Contribution

This library is open to contribution. Feel free to open issues or submit PRs. Its better to discuss issues before
submitting PRs to avoid disappointment.

### Local Development

1. Clone the repo
2. Install the system dependencies
3. Install the full dependencies with `uv sync`
4. Install the pre-commit hooks with:
   ```shell
   pre-commit install && pre-commit install --hook-type commit-msg
   ```
5. Make your changes and submit a PR

## License

This library uses the MIT license.
