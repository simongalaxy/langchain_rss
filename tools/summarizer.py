"""
Text summarization module using LangChain and Ollama.

This module provides functionality to summarize long passages of text
using local LLMs through Ollama and LangChain's text processing capabilities.
"""

from langchain_ollama import OllamaLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_core.documents import Document
from typing import Optional, List

from langdetect import detect



class TextSummarizer:
    """
    A class to summarize long text passages using Ollama and LangChain.
    
    Attributes:
        model_name: The name of the Ollama model to use (default: "llama3.2")
        temperature: Controls randomness in generation (0.0-1.0)
        chunk_size: Maximum size of text chunks for processing
        chunk_overlap: Overlap between consecutive chunks
    """
    
    def __init__(
        self,
        model_name: str = "llama3",
        temperature: float = 0.3,
        chunk_size: int = 4000,
        chunk_overlap: int = 200
    ):
        """
        Initialize the TextSummarizer.
        
        Args:
            model_name: Ollama model to use for summarization
            temperature: Temperature for text generation
            chunk_size: Size of text chunks for processing
            chunk_overlap: Overlap between chunks
        """
        self.model_name = model_name
        self.temperature = temperature
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize Ollama LLM
        self.llm = OllamaLLM(
            model=model_name,
            temperature=temperature
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    
    def summarize(
        self,
        text: str,
        method: str = "stuff",
        max_length: Optional[int] = None
    ) -> str:
        """
        Summarize a long passage of text.
        
        Args:
            text: The text to summarize
            method: Summarization method - "stuff", "map_reduce", or "refine"
            max_length: Optional maximum length for the summary
        
        Returns:
            A summarized version of the input text
        """
        # Create documents from text
        docs = self._create_documents(text)
        
        # Load the appropriate summarization chain
        chain = load_summarize_chain(
            self.llm,
            chain_type=method
        )
        
        # Generate summary
        summary = chain.run(docs)
        
        return summary.strip()
    
    def summarize_with_custom_prompt(
        self,
        text: str,
        prompt_template: Optional[str] = None
    ) -> str:
        """
        Summarize text using a custom prompt.
        
        Args:
            text: The text to summarize
            prompt_template: Custom prompt template for summarization
        
        Returns:
            A summarized version of the input text
        """
        if prompt_template is None:
            prompt_template = (
                "Please provide a concise summary of the following text, "
                "highlighting the main points and key information:\n\n{text}"
            )
        
        prompt = prompt_template.format(text=text)
        summary = self.llm.invoke(prompt)
        
        return summary.strip()
    
    def bullet_point_summary(self, text: str) -> str:
        """
        Generate a bullet-point summary of the text.
        
        Args:
            text: The text to summarize
        
        Returns:
            A bullet-point summary
        """
        
        prompt = (
            "Please summarize the following text as a list of key bullet points. "
            "Each bullet point should capture an important idea or fact:\n\n{text}"
        )
        
        return self.summarize_with_custom_prompt(text, prompt)
    
    def _create_documents(self, text: str) -> List[Document]:
        """
        Split text into documents for processing.
        
        Args:
            text: The text to split
        
        Returns:
            List of Document objects
        """
        chunks = self.text_splitter.split_text(text)
        return [Document(page_content=chunk) for chunk in chunks]


    def summarize_text(
        text: str,
        model_name: str = "llama3.2",
        method: str = "stuff"
    ) -> str:
        """
        Convenience function to quickly summarize text.
        
        Args:
            text: The text to summarize
            model_name: Ollama model to use
            method: Summarization method
        
        Returns:
            Summarized text
        """
        summarizer = TextSummarizer(model_name=model_name)
        return summarizer.summarize(text, method=method)


# if __name__ == "__main__":
#     # Example usage
#     sample_text = """
#     Artificial intelligence (AI) is intelligence demonstrated by machines, 
#     in contrast to the natural intelligence displayed by humans and animals. 
#     Leading AI textbooks define the field as the study of "intelligent agents": 
#     any device that perceives its environment and takes actions that maximize 
#     its chance of successfully achieving its goals. Colloquially, the term 
#     "artificial intelligence" is often used to describe machines (or computers) 
#     that mimic "cognitive" functions that humans associate with the human mind, 
#     such as "learning" and "problem solving".
#     """
    
#     # Initialize summarizer
#     summarizer = TextSummarizer(model_name="llama3.2")
    
#     # Generate summary
#     summary = summarizer.summarize(sample_text)
#     print("Summary:", summary)
    
#     # Generate bullet-point summary
#     bullets = summarizer.bullet_point_summary(sample_text)
#     print("\nBullet Points:", bullets)
