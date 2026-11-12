from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkManager:

    def __init__(self, config: dict):

        self.chn_config_size = config["chunking"]["chunk_size"]

        self.chn_config_overlap = config["chunking"]["chunk_overlap"]

    def chunk_markdown(self, markdown_text: str) -> list[str]:

        text_splitter = RecursiveCharacterTextSplitter(

            chunk_size=self.chn_config_size,

            chunk_overlap=self.chn_config_overlap,

            separators=["### ", "## ", "# ", "\n\n", "\n", " ", ""],

        )

        return text_splitter.split_text(markdown_text)
 