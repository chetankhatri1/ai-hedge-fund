import os
import argparse
import pandas as pd
from typing import List, Optional, Dict

from data.cache import get_cache
from data.models import (
    CompanyNews,
    FinancialMetrics,
    Price,
    LineItem,
    InsiderTrade,
)
from tools.api_providers.provider_manager import APIProviderManager

# Global cache instance
_cache = get_cache()


def get_prices(ticker: str, start_date: str, end_date: str) -> List[Price]:
    """Fetch price data from cache or API.
    
    Args:
        ticker: Stock ticker symbol
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        
    Returns:
        List of Price objects
    """
    # Get the active provider and fetch prices
    provider = APIProviderManager.get_provider()
    return provider.get_prices(ticker, start_date, end_date)


def get_financial_metrics(
    ticker: str,
    end_date: str,
    period: str = "ttm",
    limit: int = 10,
) -> List[FinancialMetrics]:
    """Fetch financial metrics from cache or API.
    
    Args:
        ticker: Stock ticker symbol
        end_date: End date in YYYY-MM-DD format
        period: Reporting period (e.g., 'ttm', 'annual', 'quarterly')
        limit: Maximum number of results to return
        
    Returns:
        List of FinancialMetrics objects
    """
    # Get the active provider and fetch financial metrics
    provider = APIProviderManager.get_provider()
    return provider.get_financial_metrics(ticker, end_date, period, limit)


def search_line_items(
    ticker: str,
    line_items: List[str],
    end_date: str,
    period: str = "ttm",
    limit: int = 10,
) -> List[LineItem]:
    """Fetch line items from API.
    
    Args:
        ticker: Stock ticker symbol
        line_items: List of line item names to search for
        end_date: End date in YYYY-MM-DD format
        period: Reporting period (e.g., 'ttm', 'annual', 'quarterly')
        limit: Maximum number of results to return
        
    Returns:
        List of LineItem objects
    """
    # Get the active provider and search for line items
    provider = APIProviderManager.get_provider()
    return provider.search_line_items(ticker, line_items, end_date, period, limit)


def get_insider_trades(
    ticker: str,
    end_date: str,
    start_date: Optional[str] = None,
    limit: int = 1000,
) -> List[InsiderTrade]:
    """Fetch insider trades from cache or API.
    
    Args:
        ticker: Stock ticker symbol
        end_date: End date in YYYY-MM-DD format
        start_date: Optional start date in YYYY-MM-DD format
        limit: Maximum number of results to return
        
    Returns:
        List of InsiderTrade objects
    """
    # Get the active provider and fetch insider trades
    provider = APIProviderManager.get_provider()
    return provider.get_insider_trades(ticker, end_date, start_date, limit)


def get_company_news(
    ticker: str,
    end_date: str,
    start_date: Optional[str] = None,
    limit: int = 1000,
) -> List[CompanyNews]:
    """Fetch company news from cache or API.
    
    Args:
        ticker: Stock ticker symbol
        end_date: End date in YYYY-MM-DD format
        start_date: Optional start date in YYYY-MM-DD format
        limit: Maximum number of results to return
        
    Returns:
        List of CompanyNews objects
    """
    # Get the active provider and fetch company news
    provider = APIProviderManager.get_provider()
    return provider.get_company_news(ticker, end_date, start_date, limit)



def get_market_cap(
    ticker: str,
    end_date: str,
) -> Optional[float]:
    """Fetch market cap from the API.
    
    Args:
        ticker: Stock ticker symbol
        end_date: End date in YYYY-MM-DD format
        
    Returns:
        Market cap value or None if not available
    """
    # Get the active provider and fetch market cap
    provider = APIProviderManager.get_provider()
    return provider.get_market_cap(ticker, end_date)


def prices_to_df(prices: List[Price]) -> pd.DataFrame:
    """Convert a list of Price objects to a pandas DataFrame.
    
    Args:
        prices: List of Price objects
        
    Returns:
        DataFrame with price data
    """
    df = pd.DataFrame([p.model_dump() for p in prices])
    df["Date"] = pd.to_datetime(df["time"])
    df.set_index("Date", inplace=True)
    numeric_cols = ["open", "close", "high", "low", "volume"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df.sort_index(inplace=True)
    return df


def get_price_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch price data and convert to a pandas DataFrame.
    
    Args:
        ticker: Stock ticker symbol
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        
    Returns:
        DataFrame with price data
    """
    prices = get_prices(ticker, start_date, end_date)
    return prices_to_df(prices)


def get_available_providers() -> Dict[str, str]:
    """
    Get a dictionary of available API providers.
    
    Returns:
        Dictionary mapping provider keys to provider names
    """
    return APIProviderManager.get_available_providers()


def get_current_provider() -> str:
    """
    Get the key of the currently active API provider.
    
    Returns:
        Provider key as a string
    """
    provider = APIProviderManager.get_provider()
    for key, cls in APIProviderManager._providers.items():
        if isinstance(provider, cls):
            return key
    return "unknown"


def set_api_provider(provider_name: str) -> None:
    """
    Set the active API provider by name.
    
    Args:
        provider_name: Name of the provider to set as active
    """
    APIProviderManager.set_provider(provider_name)


def parse_api_provider_args():
    """
    Parse command-line arguments for API provider selection.
    This can be used to add API provider selection to existing scripts.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(description="API Provider Selection")
    parser.add_argument(
        "--api-provider", 
        type=str,
        choices=list(get_available_providers().keys()),
        help="API provider to use for financial data"
    )
    
    # Parse known args only, so it can be used alongside other argument parsers
    args, _ = parser.parse_known_args()
    
    # Set the API provider if specified
    if args.api_provider:
        set_api_provider(args.api_provider)
    
    return args
