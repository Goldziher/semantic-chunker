from __future__ import annotations

from json import JSONDecodeError, loads
from pathlib import Path
from typing import Any, Callable, Literal, Protocol, cast, overload

from semantic_text_splitter import CodeSplitter, MarkdownSplitter, TextSplitter
from tree_sitter_language_pack import SupportedLanguage, get_binding
from typing_extensions import Never

try:
    from tokenizers import Tokenizer  # type: ignore[import-untyped]
except ImportError:
    # We ensure that type checkers will never match this if 'tokenizers' is not installed.
    Tokenizer = Never

_splitters_kw_map: dict[Literal["text", "markdown", "code"], type[TextSplitter | MarkdownSplitter | CodeSplitter]] = {
    "text": TextSplitter,
    "markdown": MarkdownSplitter,
    "code": CodeSplitter,
}

Callback = Callable[[str], int]

__all__ = ["SemanticChunker", "get_chunker"]


class SemanticChunker(Protocol):
    """A protocol representing a semantic chunker."""

    def chunks(self, content: str) -> list[str]:
        """Generate a list of chunks from a given text. Each chunk will be up to the `capacity`.

        Args:
            content: The text to chunk.

        Returns:
            A list of chunks.
        """
        ...

    def chunk_with_indices(self, content: str) -> list[tuple[int, str]]:
        """Generate a list of chunks from a given text, along with their character offsets in the original text. Each chunk will be up to the `capacity`.

        Args:
            content: The text to chunk.

        Returns:
            A list of chunks.
        """
        ...


def _is_valid_json(content: Any) -> bool:
    try:
        loads(content)
        return True
    except JSONDecodeError:
        return False


def _is_json_file_path(content: str) -> bool:
    return content.endswith(".json")


@overload
def get_chunker(  # type: ignore[no-any-unimported]
    model: str | Tokenizer | Callback | Path,
    *,
    chunking_type: Literal["text"],
    max_tokens: int | tuple[int, int],
    overlap: int,
    trim: bool,
) -> SemanticChunker: ...


@overload
def get_chunker(  # type: ignore[no-any-unimported]
    model: str | Tokenizer | Callback | Path,
    *,
    chunking_type: Literal["markdown"],
    max_tokens: int | tuple[int, int],
    overlap: int,
    trim: bool,
) -> SemanticChunker: ...


@overload
def get_chunker(  # type: ignore[no-any-unimported]
    model: str | Tokenizer | Callback | Path,
    *,
    chunking_type: Literal["code"],
    language: SupportedLanguage,
    max_tokens: int | tuple[int, int],
    overlap: int,
    trim: bool,
) -> SemanticChunker: ...


def get_chunker(  # type: ignore[no-any-unimported]
    model: str | Tokenizer | Callback | Path,
    *,
    chunking_type: Literal["text", "markdown", "code"],
    language: SupportedLanguage | None = None,
    max_tokens: int | tuple[int, int],
    overlap: int = 0,
    trim: bool = True,
) -> SemanticChunker:
    """Get the chunker for the given chunking type.

    Args:
        model: The model name or tokenizer.
        chunking_type: The type of content to chunk.
        language: The coding language to chunk - if the content is code.
        max_tokens: The maximal number of tokens per chunk.
        overlap: The number of allowed to overlap between chunks.
        trim: Whether to trim whitespace

    Raises:
        ValueError: If the language is not provided for code chunking.

    Returns:
        The chunker for the given chunking type.
    """
    chunker_cls = _splitters_kw_map[chunking_type]

    kwargs = {
        "capacity": max_tokens,
        "overlap": overlap,
        "trim": trim,
    }

    if chunking_type == "code":
        if language is None:
            raise ValueError("Language must be provided for code chunking.")

        kwargs["language"] = get_binding(language)

    if isinstance(model, Tokenizer):
        chunker = chunker_cls.from_huggingface_tokenizer(tokenizer=model, **kwargs)  # type: ignore[arg-type]
    elif callable(model):
        chunker = chunker_cls.from_callback(callback=model, **kwargs)  # type: ignore[arg-type]
    elif _is_valid_json(model):
        chunker = chunker_cls.from_huggingface_tokenizer_str(json=model, **kwargs)  # type: ignore[arg-type]
    elif isinstance(model, Path) or _is_json_file_path(model):
        chunker = chunker_cls.from_huggingface_tokenizer_file(path=str(model), **kwargs)  # type: ignore[arg-type]
    else:
        chunker = chunker_cls.from_tiktoken_model(model=model, **kwargs)  # type: ignore[arg-type]

    return cast(SemanticChunker, chunker)
