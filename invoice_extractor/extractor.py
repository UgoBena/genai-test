import pymupdf
import pymupdf4llm
from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import JsonOutputParser

from invoice_extractor.config import settings
from invoice_extractor.prompt import prompt_template


class InvoiceExtractor:
    """Class extract text from PDF and runs inference using MistralAI platform"""
    def __init__(self):
        self.llm = ChatMistralAI(
            model=settings.mistral_model,
            api_key=settings.mistral_api_key,
            temperature=settings.mistral_model_temperature,
        )

    def extract_text(self, pdf_file: bytes) -> str:
        """Extract markdown from in memory pdf"""
        document = pymupdf.Document(stream=pdf_file)
        return pymupdf4llm.to_markdown(document)

    def process(self, pdf_file: bytes) -> dict:
        """Extract information using prompt template on in-memory pdf"""
        chain = prompt_template | self.llm | JsonOutputParser()
        invoice_text = self.extract_text(pdf_file)
        return chain.invoke({"invoice_text": invoice_text})
