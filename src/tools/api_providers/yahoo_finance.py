"""
Yahoo Finance API Provider implementation.
"""
import os
import json
import requests
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import pandas as pd

from data.cache import get_cache
from data.models import (
    CompanyNews,
    FinancialMetrics,
    Price,
    LineItem,
    InsiderTrade,
)
from .base import BaseAPIProvider

# Global cache instance
_cache = get_cache()


class YahooFinanceProvider(BaseAPIProvider):
    """Yahoo Finance API provider implementation."""
    
    @property
    def name(self) -> str:
        return "Yahoo Finance API"
    
    def _get_headers(self) -> dict:
        """Get API headers with authentication."""
        headers = {
            "X-API-KEY": os.environ.get("YAHOO_FINANCE_API_KEY", ""),
            "Content-Type": "application/json",
        }
        return headers
    
    def get_prices(self, ticker: str, start_date: str, end_date: str) -> List[Price]:
        """Fetch price data from cache or Yahoo Finance API."""
        # Check cache first
        if cached_data := _cache.get_prices(ticker):
            # Filter cached data by date range and convert to Price objects
            filtered_data = [Price(**price) for price in cached_data if start_date <= price["time"] <= end_date]
            if filtered_data:
                return filtered_data

        # Convert dates to UNIX timestamps for Yahoo Finance
        start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
        end_timestamp = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())
        
        # Yahoo Finance API endpoint
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?period1={start_timestamp}&period2={end_timestamp}&interval=1d"
        
        response = requests.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise Exception(f"Error fetching data: {ticker} - {response.status_code} - {response.text}")
        
        data = response.json()
        result = data.get("chart", {}).get("result", [{}])[0]
        
        if not result:
            return []
        
        # Extract price data
        timestamps = result.get("timestamp", [])
        quote = result.get("indicators", {}).get("quote", [{}])[0]
        
        prices = []
        for i, timestamp in enumerate(timestamps):
            # Convert UNIX timestamp to ISO format
            time_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%dT%H:%M:%SZ")
            
            price = Price(
                ticker=ticker,
                open=quote.get("open", [])[i] if i < len(quote.get("open", [])) else None,
                high=quote.get("high", [])[i] if i < len(quote.get("high", [])) else None,
                low=quote.get("low", [])[i] if i < len(quote.get("low", [])) else None,
                close=quote.get("close", [])[i] if i < len(quote.get("close", [])) else None,
                volume=quote.get("volume", [])[i] if i < len(quote.get("volume", [])) else None,
                time=time_str,
                time_milliseconds=timestamp * 1000
            )
            prices.append(price)
        
        # Cache the results as dicts
        _cache.set_prices(ticker, [p.model_dump() for p in prices])
        return prices
    
    def get_financial_metrics(
        self, 
        ticker: str,
        end_date: str,
        period: str = "ttm",
        limit: int = 10,
    ) -> List[FinancialMetrics]:
        """Fetch financial metrics from cache or Yahoo Finance API."""
        # Check cache first
        if cached_data := _cache.get_financial_metrics(ticker):
            # Filter cached data by date and limit
            filtered_data = [FinancialMetrics(**metric) for metric in cached_data if metric["report_period"] <= end_date]
            filtered_data.sort(key=lambda x: x.report_period, reverse=True)
            if filtered_data:
                return filtered_data[:limit]

        # Yahoo Finance API endpoint for financial data
        url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=financialData,defaultKeyStatistics,summaryDetail"
        
        response = requests.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise Exception(f"Error fetching data: {ticker} - {response.status_code} - {response.text}")
        
        data = response.json()
        result = data.get("quoteSummary", {}).get("result", [{}])[0]
        
        if not result:
            return []
        
        # Extract financial data
        financial_data = result.get("financialData", {})
        key_stats = result.get("defaultKeyStatistics", {})
        summary_detail = result.get("summaryDetail", {})
        
        # Create a FinancialMetrics object
        report_date = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        
        metrics = FinancialMetrics(
            ticker=ticker,
            report_period=report_date,
            period=period,
            revenue=financial_data.get("totalRevenue", {}).get("raw"),
            gross_profit=financial_data.get("grossProfits", {}).get("raw") if financial_data.get("grossProfits") else None,
            operating_income=financial_data.get("operatingIncome", {}).get("raw") if financial_data.get("operatingIncome") else None,
            net_income=financial_data.get("netIncome", {}).get("raw") if financial_data.get("netIncome") else None,
            eps_basic=key_stats.get("trailingEps", {}).get("raw") if key_stats.get("trailingEps") else None,
            eps_diluted=key_stats.get("trailingEps", {}).get("raw") if key_stats.get("trailingEps") else None,
            dividend_yield=summary_detail.get("dividendYield", {}).get("raw") if summary_detail.get("dividendYield") else None,
            book_value_per_share=key_stats.get("bookValue", {}).get("raw") if key_stats.get("bookValue") else None,
            market_cap=financial_data.get("marketCap", {}).get("raw") if financial_data.get("marketCap") else None,
            pe_ratio=summary_detail.get("trailingPE", {}).get("raw") if summary_detail.get("trailingPE") else None,
            price_to_book=key_stats.get("priceToBook", {}).get("raw") if key_stats.get("priceToBook") else None,
            debt_to_equity=financial_data.get("debtToEquity", {}).get("raw") if financial_data.get("debtToEquity") else None,
            free_cash_flow=financial_data.get("freeCashflow", {}).get("raw") if financial_data.get("freeCashflow") else None,
            operating_cash_flow=financial_data.get("operatingCashflow", {}).get("raw") if financial_data.get("operatingCashflow") else None,
            ebitda=financial_data.get("ebitda", {}).get("raw") if financial_data.get("ebitda") else None,
            total_debt=financial_data.get("totalDebt", {}).get("raw") if financial_data.get("totalDebt") else None,
            return_on_equity=financial_data.get("returnOnEquity", {}).get("raw") if financial_data.get("returnOnEquity") else None,
            return_on_assets=financial_data.get("returnOnAssets", {}).get("raw") if financial_data.get("returnOnAssets") else None,
            profit_margin=financial_data.get("profitMargins", {}).get("raw") if financial_data.get("profitMargins") else None,
            operating_margin=financial_data.get("operatingMargins", {}).get("raw") if financial_data.get("operatingMargins") else None,
            current_ratio=financial_data.get("currentRatio", {}).get("raw") if financial_data.get("currentRatio") else None,
            quick_ratio=None,  # Not directly available in Yahoo Finance
            total_assets=None,  # Not directly available in Yahoo Finance
            total_liabilities=None,  # Not directly available in Yahoo Finance
            shares_outstanding=key_stats.get("sharesOutstanding", {}).get("raw") if key_stats.get("sharesOutstanding") else None,
        )
        
        # Cache the result
        _cache.set_financial_metrics(ticker, [metrics.model_dump()])
        return [metrics]
    
    def search_line_items(
        self,
        ticker: str,
        line_items: List[str],
        end_date: str,
        period: str = "ttm",
        limit: int = 10,
    ) -> List[LineItem]:
        """Fetch specific line items from Yahoo Finance API."""
        # Yahoo Finance doesn't have a direct equivalent to the line items API
        # We'll fetch the financial statements and extract the requested items
        
        url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=incomeStatementHistory,balanceSheetHistory,cashflowStatementHistory"
        
        response = requests.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise Exception(f"Error fetching data: {ticker} - {response.status_code} - {response.text}")
        
        data = response.json()
        result = data.get("quoteSummary", {}).get("result", [{}])[0]
        
        if not result:
            return []
        
        # Extract financial statements
        income_stmt = result.get("incomeStatementHistory", {}).get("incomeStatementHistory", [])
        balance_sheet = result.get("balanceSheetHistory", {}).get("balanceSheetStatements", [])
        cash_flow = result.get("cashflowStatementHistory", {}).get("cashflowStatements", [])
        
        # Combine all statements into a single dictionary for easier lookup
        statements = {}
        for stmt in income_stmt + balance_sheet + cash_flow:
            end_date_raw = stmt.get("endDate", {}).get("fmt")
            if end_date_raw:
                stmt_date = datetime.strptime(end_date_raw, "%Y-%m-%d").strftime("%Y-%m-%d")
                if stmt_date not in statements:
                    statements[stmt_date] = {}
                statements[stmt_date].update(stmt)
        
        # Create LineItem objects for the requested line items
        results = []
        for date, stmt in statements.items():
            if date <= end_date:  # Only include statements on or before the end date
                for item_name in line_items:
                    # Try to find the item in the statement
                    item_value = None
                    for key, value in stmt.items():
                        if key.lower().replace("_", "") == item_name.lower().replace("_", ""):
                            item_value = value.get("raw") if isinstance(value, dict) and "raw" in value else value
                            break
                    
                    if item_value is not None:
                        line_item = LineItem(
                            ticker=ticker,
                            line_item=item_name,
                            value=item_value,
                            report_period=date,
                            period=period,
                        )
                        results.append(line_item)
        
        # Sort by date (newest first) and limit results
        results.sort(key=lambda x: x.report_period, reverse=True)
        return results[:limit]
    
    def get_insider_trades(
        self,
        ticker: str,
        end_date: str,
        start_date: Optional[str] = None,
        limit: int = 1000,
    ) -> List[InsiderTrade]:
        """Fetch insider trades from cache or Yahoo Finance API."""
        # Check cache first
        if cached_data := _cache.get_insider_trades(ticker):
            # Filter cached data by date range
            filtered_data = [InsiderTrade(**trade) for trade in cached_data 
                            if (start_date is None or (trade.get("transaction_date") or trade["filing_date"]) >= start_date)
                            and (trade.get("transaction_date") or trade["filing_date"]) <= end_date]
            filtered_data.sort(key=lambda x: x.transaction_date or x.filing_date, reverse=True)
            if filtered_data:
                return filtered_data

        # Yahoo Finance API endpoint for insider trades
        url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=insiderTransactions"
        
        response = requests.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise Exception(f"Error fetching data: {ticker} - {response.status_code} - {response.text}")
        
        data = response.json()
        transactions = data.get("quoteSummary", {}).get("result", [{}])[0].get("insiderTransactions", {}).get("transactions", [])
        
        if not transactions:
            return []
        
        insider_trades = []
        for tx in transactions:
            # Parse the transaction date
            tx_date = tx.get("startDate", {}).get("fmt")
            if not tx_date:
                continue
                
            tx_date_obj = datetime.strptime(tx_date, "%Y-%m-%d")
            tx_date_str = tx_date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")
            
            # Skip if outside date range
            if (start_date and tx_date < start_date) or tx_date > end_date:
                continue
            
            # Create InsiderTrade object
            insider_trade = InsiderTrade(
                ticker=ticker,
                transaction_date=tx_date_str,
                filing_date=tx_date_str,  # Yahoo doesn't provide separate filing date
                insider_name=tx.get("filerName", ""),
                insider_title=tx.get("filerRelation", ""),
                transaction_type=tx.get("transactionDescription", ""),
                shares=tx.get("shares", {}).get("raw") if tx.get("shares") else None,
                share_price=tx.get("value", {}).get("raw") / tx.get("shares", {}).get("raw") if tx.get("value") and tx.get("shares") else None,
                value=tx.get("value", {}).get("raw") if tx.get("value") else None,
                shares_owned_after=None,  # Not provided by Yahoo
                sec_form=tx.get("filerUrl", "").split("/")[-1] if tx.get("filerUrl") else None,
            )
            insider_trades.append(insider_trade)
        
        # Cache the results
        _cache.set_insider_trades(ticker, [trade.model_dump() for trade in insider_trades])
        return insider_trades
    
    def get_company_news(
        self,
        ticker: str,
        end_date: str,
        start_date: Optional[str] = None,
        limit: int = 1000,
    ) -> List[CompanyNews]:
        """Fetch company news from cache or Yahoo Finance API."""
        # Check cache first
        if cached_data := _cache.get_company_news(ticker):
            # Filter cached data by date range
            filtered_data = [CompanyNews(**news) for news in cached_data 
                            if (start_date is None or news["date"] >= start_date)
                            and news["date"] <= end_date]
            filtered_data.sort(key=lambda x: x.date, reverse=True)
            if filtered_data:
                return filtered_data

        # Yahoo Finance API endpoint for news
        url = f"https://query2.finance.yahoo.com/v2/finance/news?symbol={ticker}"
        
        response = requests.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise Exception(f"Error fetching data: {ticker} - {response.status_code} - {response.text}")
        
        data = response.json()
        news_items = data.get("items", {}).get("result", [])
        
        if not news_items:
            return []
        
        company_news = []
        for item in news_items:
            # Parse the publication date
            pub_date = datetime.fromtimestamp(item.get("published_at", 0))
            pub_date_str = pub_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            pub_date_only = pub_date.strftime("%Y-%m-%d")
            
            # Skip if outside date range
            if (start_date and pub_date_only < start_date) or pub_date_only > end_date:
                continue
            
            # Create CompanyNews object
            news = CompanyNews(
                ticker=ticker,
                date=pub_date_str,
                title=item.get("title", ""),
                summary=item.get("summary", ""),
                url=item.get("link", ""),
                source=item.get("publisher", ""),
                sentiment=None,  # Yahoo doesn't provide sentiment analysis
            )
            company_news.append(news)
            
            # Stop if we've reached the limit
            if len(company_news) >= limit:
                break
        
        # Cache the results
        _cache.set_company_news(ticker, [news.model_dump() for news in company_news])
        return company_news
    
    def get_market_cap(
        self,
        ticker: str,
        end_date: str,
    ) -> Optional[float]:
        """Fetch market cap from Yahoo Finance API."""
        financial_metrics = self.get_financial_metrics(ticker, end_date)
        if not financial_metrics:
            return None
        market_cap = financial_metrics[0].market_cap
        if not market_cap:
            return None
        return market_cap
