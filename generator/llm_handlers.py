"""
LLM Handlers for different providers (Ollama, Groq)
"""

import os
import logging
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod
from django.conf import settings

try:
    from langchain_ollama import ChatOllama
    from langchain_groq import ChatGroq
    from langchain.schema import HumanMessage, SystemMessage
    LANGCHAIN_AVAILABLE = True
except Exception as e:
    print(f"Error importing LangChain: {e}")
    LANGCHAIN_AVAILABLE = False

logger = logging.getLogger(__name__)


class BaseLLMHandler(ABC):
    """Base class for LLM handlers"""
    
    @abstractmethod
    def generate_response(self, prompt: str, system_message: Optional[str] = None) -> str:
        """Generate response from LLM"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the LLM provider is available"""
        pass


class OllamaLLMHandler(BaseLLMHandler):
    """Ollama LLM handler for local models"""
    
    def __init__(self, model_name: str = "llama2"):
        self.model_name = model_name
        self.llm = None
        self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize the Ollama LLM"""
        if not LANGCHAIN_AVAILABLE:
            raise ImportError("LangChain not available. Please install langchain-ollama.")
        
        try:
            # Use base URL from Django settings
            base_url = getattr(settings, 'OLLAMA_BASE_URL', 'http://localhost:11434')
            self.llm = ChatOllama(model=self.model_name, base_url=base_url)
            logger.info(f"Initialized Ollama with model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Ollama: {e}")
            raise RuntimeError(f"Failed to initialize Ollama with model {self.model_name}: {e}")
    
    def generate_response(self, prompt: str, system_message: Optional[str] = None) -> str:
        """Generate response using Ollama"""
        if not self.llm:
            raise RuntimeError("Ollama LLM not initialized")
        
        try:
            messages = []
            if system_message:
                messages.append(SystemMessage(content=system_message))
            messages.append(HumanMessage(content=prompt))
            
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"Error generating response with Ollama: {e}")
            raise RuntimeError(f"Error generating response with Ollama: {e}")
    
    def is_available(self) -> bool:
        """Check if Ollama is available"""
        return self.llm is not None


class GroqLLMHandler(BaseLLMHandler):
    """Groq LLM handler for cloud models"""
    
    def __init__(self, model_name: str = "llama3-8b-8192"):
        self.model_name = model_name
        self.llm = None
        self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize the Groq LLM"""
        if not LANGCHAIN_AVAILABLE:
            raise ImportError("LangChain not available. Please install langchain-groq.")
        
        # Get API key from Django settings
        api_key = getattr(settings, 'GROQ_API_KEY', None)
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")
        
        try:
            self.llm = ChatGroq(
                groq_api_key=api_key,
                model_name=self.model_name
            )
            logger.info(f"Initialized Groq with model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Groq: {e}")
            raise RuntimeError(f"Failed to initialize Groq with model {self.model_name}: {e}")
    
    def generate_response(self, prompt: str, system_message: Optional[str] = None) -> str:
        """Generate response using Groq"""
        if not self.llm:
            raise RuntimeError("Groq LLM not initialized")
        
        try:
            messages = []
            if system_message:
                messages.append(SystemMessage(content=system_message))
            messages.append(HumanMessage(content=prompt))
            
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"Error generating response with Groq: {e}")
            raise RuntimeError(f"Error generating response with Groq: {e}")
    
    def is_available(self) -> bool:
        """Check if Groq is available"""
        return self.llm is not None and getattr(settings, 'GROQ_API_KEY', None) is not None


def get_llm_handler(provider: str, model_name: str) -> BaseLLMHandler:
    """Factory function to get the appropriate LLM handler"""
    if provider == "ollama":
        return OllamaLLMHandler(model_name)
    elif provider == "groq":
        return GroqLLMHandler(model_name)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}. Only 'groq' and 'ollama' are supported.") 