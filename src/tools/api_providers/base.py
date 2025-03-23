"""
Base API Provider interface for the AI Hedge Fund.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from data.models import (
    Price,
    FinancialMetrics,
    LineItem,
    InsiderTrade,
    CompanyNews,
)


class BaseAPIProvider(ABC):
    """Base interface for all API providers."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the API provider."""
        pass
    
    @abstractmethod
    def get_prices(self, ticker: str, start_date: str, end_date: str) -> List[Price]:
        """Fetch price data for a ticker within a date range."""
        pass
    
    @abstractmethod
    def get_financial_metrics(
        self, 
        ticker: str,
        end_date: str,
        period: str = "ttm",
        limit: int = 10,
    ) -> List[FinancialMetrics]:
        """Fetch financial metrics for a ticker."""
        pass
    
    @abstractmethod
    def search_line_items(
        self,
        ticker: str,
        line_items: List[str],
        end_date: str,
        period: str = "ttm",
        limit: int = 10,
    ) -> List[LineItem]:
        """Fetch specific line items for a ticker."""
        pass
    
    @abstractmethod
    def get_insider_trades(
        self,
        ticker: str,
        end_date: str,
        start_date: Optional[str] = None,
        limit: int = 1000,
    ) -> List[InsiderTrade]:
        """Fetch insider trades for a ticker."""
        pass
    
    @abstractmethod
    def get_company_news(
        self,
        ticker: str,
        end_date: str,
        start_date: Optional[str] = None,
        limit: int = 1000,
    ) -> List[CompanyNews]:
        """Fetch company news for a ticker."""
        pass
    
    @abstractmethod
    def get_market_cap(
        self,
        ticker: str,
        end_date: str,
    ) -> Optional[float]:
        """Fetch market cap for a ticker."""
        pass
