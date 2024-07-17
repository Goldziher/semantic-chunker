# semantic-chunker

This library is built on top of the [semantic-text-splitter](https://github.com/benbrandt/text-splitter)
library, written in Rust, combining it with
the [tree-sitter-language-pack](https://github.com/Goldziher/tree-sitter-language-pack)
to enable code-splitting.

Its main utility is in providing a strongly typed interface to the underlying library and removing the need for
managing
tree-sitter dependencies.

## Installation

```shell
pip install semantic-chunker
```

Or to include the optional `tokenizers` dependency:

```shell
pip install semantic-chunker[tokenizers]
```

### Usage

Import the `get_chunker` function from the `semantic_chunker` module, and use it to get a chunker instance and chunk
content. You can chunk plain text:

```python
from semantic_chunker import get_chunker

plain_text = """
Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin
literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney
College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage,
and going through the cites of the word in classical literature, discovered the undoubtable source: Lorem Ipsum
comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by
Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance.
The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section
"""

chunker = get_chunker(
    "gpt-3.5-turbo",
    chunking_type="text",  # required
    max_tokens=10,  # required
    trim=False,  # default True
    overlap=5,  # default 0
)

# Then use it to chunk a value into either a list of chunks that are up to the `max_tokens` length:
chunks = chunker.chunks(plain_text)  # list[str]

# Or a list of tuples containing the character offset indices and the chunk:
chunks_with_incides = chunker.chunk_with_indices(plain_text)  # list[tuple[str, int]]
```

Markdown:

```python
from semantic_chunker import get_chunker

markdown_text = """
# Lorem Ipsum Intro


Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature
from 45 BC, making it over 2000 years old.


Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin
words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature,
discovered the undoubtable source: Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum"
(The Extremes of Good and Evil) by Cicero, written in 45 BC.
This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum,
"Lorem ipsum dolor sit amet..", comes from a line in section.
"""

chunker = get_chunker(
    "gpt-3.5-turbo",
    chunking_type="markdown",  # required
    max_tokens=10,  # required
    trim=False,  # default True
    overlap=5,  # default 0
)

# Then use it to chunk a value into either a list of chunks that are up to the `max_tokens` length:
chunks = chunker.chunks(markdown_text)  # list[str]

# Or a list of tuples containing the character offset indices and the chunk:
chunks_with_incides = chunker.chunk_with_indices(markdown_text)  # list[tuple[str, int]]
```

Or code:

```python
from semantic_chunker import get_chunker

kotlin_snippet = """
import kotlin.random.Random


fun main() {
 val randomNumbers = IntArray(10) { Random.nextInt(1, 100) } // Generate an array of 10 random integers between 1 and 99
 println("Random numbers:")
 for (number in randomNumbers) {
     println(number)  // Print each random number
 }
}
"""

chunker = get_chunker(
    "gpt-3.5-turbo",
    chunking_type="code",  # required
    max_tokens=10,  # required
    language="kotlin",  # required, only for code chunking, ignored otherwise
    trim=False,  # default True
    overlap=5,  # default 0
)

# Then use it to chunk a value into either a list of chunks that are up to the `max_tokens` length:
chunks = chunker.chunks(kotlin_snippet)  # list[str]

# Or a list of tuples containing the character offset indices and the chunk:
chunks_with_incides = chunker.chunk_with_indices(kotlin_snippet)  # list[tuple[str, int]]
```

The first argument to `get_chunker` is a required argument (not kwarg), which can be one of the following:

1. a tiktoken model string identifier (e.g. `gpt-3.5-turbo` etc.)
2. a callback function that receives a text (string) and returns the number of tokens it contains (integer.)
3. a `tokenizers.Tokenizer` instance (or an instance of a subclass thereof).
4. a file path to a tokenizer JSON file as a string (`"/path/to/tokenizer.json"`) or `Path`
   instance (`Path("/path/to/tokenizer.json")`)

The (**required**) kwarg `chunking_type` can be either `text`, `markdown` or `code`.
The (**required**) kwarg `max_tokens` is the maximum number of tokens in each chunk. This kwarg accepts either an _
_integer__ or a __tuple__ of two integers (`tuple[int,int]`), which represents a min/max range within which the number
of tokens in each chunk should fall.

If the `chunking_type` is `code`, the `language` kwarg is **required**. This kwarg should be a string representing the
language of the code to be split. The language should be one of the languages included in the
the `tree-sitter-language-pack` library,
([see here for a list](https://github.com/Goldziher/tree-sitter-language-pack)).

### Note on Types

The [semantic-text-splitter](https://github.com/benbrandt/text-splitter) library is used to split the text into chunks (
very fast). It has 3 types of splitters: `TextSplitter`, `MarkdownSplitter`, and `CodeSplitter`. This is abstracted by
this library into a protocol type named `SemanticChunker`:

```python
from typing import Protocol


class SemanticChunker(Protocol):
    def chunks(self, content: str) -> list[str]:
        """Generate a list of chunks from a given text. Each chunk will be up to the `capacity`."""

    def chunk_with_indices(self, content: str) -> list[tuple[int, str]]:
        """Generate a list of chunks from a given text, along with their character offsets in the original text. Each chunk will be up to the `capacity`."""
```

## Contribution

This library welcomes contributions. To contribute, please follow the steps below:

1. Fork and clone the repository.
2. Make changes and commit them (follow [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)).
3. Submit a PR.

Read below on how to develop locally:

### Prerequisites

- A compatible Python version.
- [pdm](https://github.com/pdm-project/pdm) installed.
- [pre-commit](https://pre-commit.com) installed.

### Setup

1. Inside the repository, install the dependencies with:

  ```shell
    pdm install
  ```

This will create a virtual env under the git ignored `.venv` folder and install all the dependencies.

2. Install the pre-commit hooks:

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

### Updating Dependencies

To update the dependencies, run:

```shell
  pdm update
```
