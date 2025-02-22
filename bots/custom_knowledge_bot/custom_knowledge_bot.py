import os
import fitz  # PyMuPDF for PDF text extraction
from haystack import Pipeline, Document
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.fetchers import LinkContentFetcher
from haystack.components.converters import HTMLToDocument
from haystack.components.writers import DocumentWriter
from haystack.utils import Secret


class CustomKnowledgeBot:
    def __init__(self, config: dict, bot_token: str):
        self.knowledge_urls = config.get("knowledge_urls", [])
        self.file_paths = config.get("file_paths", [])
        self.bot_token = bot_token

        # Initialize Haystack document store
        self.document_store = InMemoryDocumentStore()

        # Load knowledge from files
        self.load_knowledge()

        # Build the pipeline
        self.pipeline = self.build_pipeline()

    def load_knowledge(self):
        """Extract knowledge from PDFs and store it in the document store."""
        documents = []

        # Extract text from PDFs
        for file_path in self.file_paths:
            file_text = self.extract_text_from_file(file_path)
            documents.append(Document(content=file_text, meta={"source": file_path}))

        # Store documents in the Haystack document store
        if documents:
            self.document_store.write_documents(documents)

    def extract_text_from_file(self, file_path):
        """Extract text from a given file."""
        if file_path.endswith(".pdf"):
            return self.extract_text_from_pdf(file_path)
        else:
            return open(file_path, "r").read()

    def extract_text_from_pdf(self, pdf_path):
        """Extract text from a given PDF file."""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text("text") + "\n"
            return text if text else None
        except Exception as e:
            print(f"Error reading {pdf_path}: {e}")
            return None

    def build_pipeline(self):
        """Build the Haystack pipeline for fetching and answering questions."""
        # Build a RAG pipeline
        prompt_template = """
        Given these documents, answer the question.
        Documents:
        {% for doc in documents %}
            {{ doc.content }}
        {% endfor %}
        Question: {{question}}
        Answer:
        """

        fetcher = LinkContentFetcher()
        converter = HTMLToDocument()
        writer = DocumentWriter(document_store=self.document_store)

        indexing_pipeline = Pipeline()

        indexing_pipeline.add_component(instance=fetcher, name="fetcher")
        indexing_pipeline.add_component(instance=converter, name="converter")
        indexing_pipeline.add_component(instance=writer, name="writer")

        indexing_pipeline.connect("fetcher.streams", "converter.sources")
        indexing_pipeline.connect("converter.documents", "writer.documents")
        indexing_pipeline.run({"fetcher": {"urls": self.knowledge_urls}})

        retriever = InMemoryBM25Retriever(document_store=self.document_store)
        prompt_builder = PromptBuilder(template=prompt_template)
        llm = OpenAIGenerator(api_key=Secret.from_token(os.getenv("OPENAI_API_KEY")))

        rag_pipeline = Pipeline()

        rag_pipeline.add_component(instance=retriever, name="retriever")
        rag_pipeline.add_component(instance=prompt_builder, name="prompt_builder")
        rag_pipeline.add_component(instance=llm, name="llm")

        rag_pipeline.connect("retriever", "prompt_builder.documents")
        rag_pipeline.connect("prompt_builder", "llm")

        return rag_pipeline

    def process_message_text(self, message: str) -> str:
        result = self.pipeline.run(
            {
                "retriever": {"query": message},
                "prompt_builder": {"question": message},
            }
        )
        return result["llm"]["replies"][0]
