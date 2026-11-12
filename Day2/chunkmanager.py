
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter


class ChunkManager:

    def chunk_markdown(
        self,
        markdown_text: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ) -> list[str]:

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["### ", "## ", "# ", "\n\n", "\n", " ", ""],
        )

        return text_splitter.split_text(markdown_text)
