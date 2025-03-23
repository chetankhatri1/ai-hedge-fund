"""
API Provider Manager for the AI Hedge Fund.
This module provides a way to switch between different financial data API providers.
"""
import os
from typing import Dict, Type, Optional

from .base import BaseAPIProvider
from .financial_datasets import FinancialDatasetsProvider
from .yahoo_finance import YahooFinanceProvider


class APIProviderManager:
    """Manager for API providers."""
    
    # Available providers
    _providers: Dict[str, Type[BaseAPIProvider]] = {
        "financial_datasets": FinancialDatasetsProvider,
        "yahoo_finance": YahooFinanceProvider,
    }
    
    # Current active provider instance
    _active_provider: Optional[BaseAPIProvider] = None
    
    @classmethod
    def get_provider(cls) -> BaseAPIProvider:
        """Get the active API provider."""
        if cls._active_provider is None:
            # Initialize with the default provider
            cls.set_provider(cls._get_default_provider())
        return cls._active_provider
    
    @classmethod
    def set_provider(cls, provider_name: str) -> None:
        """Set the active API provider by name."""
        if provider_name not in cls._providers:
            raise ValueError(f"Unknown provider: {provider_name}. Available providers: {list(cls._providers.keys())}")
        
        cls._active_provider = cls._providers[provider_name]()
    
    @classmethod
    def _get_default_provider(cls) -> str:
        """Get the default provider based on available API keys."""
        # Check environment variables for API keys
        if os.environ.get("FINANCIAL_DATASETS_API_KEY"):
            return "financial_datasets"
        elif os.environ.get("YAHOO_FINANCE_API_KEY"):
            return "yahoo_finance"
        else:
            # Default to Financial Datasets if no API keys are found
            return "financial_datasets"
    
    @classmethod
    def get_available_providers(cls) -> Dict[str, str]:
        """Get a dictionary of available providers with their names."""
        return {
            provider_key: provider_cls().name
            for provider_key, provider_cls in cls._providers.items()
        }
