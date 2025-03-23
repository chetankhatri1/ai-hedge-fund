#!/usr/bin/env python3
"""
API Provider Demo Script

This script demonstrates the API provider switching functionality.
It allows fetching financial data from different API providers.
"""
import os
import sys
import argparse
import pandas as pd
from datetime import datetime, timedelta

from tools.api import (
    get_prices,
    get_financial_metrics,
    get_company_news,
    get_insider_trades,
    get_market_cap,
    get_price_data,
    get_available_providers,
    get_current_provider,
    set_api_provider,
)


def format_date(date_obj):
    """Format a date object to YYYY-MM-DD string."""
    return date_obj.strftime("%Y-%m-%d")


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="API Provider Demo")
    parser.add_argument(
        "--ticker", 
        type=str, 
        default="AAPL",
        help="Stock ticker symbol to fetch data for"
    )
    parser.add_argument(
        "--api-provider", 
        type=str,
        choices=list(get_available_providers().keys()),
        help="API provider to use for financial data"
    )
    parser.add_argument(
        "--days", 
        type=int, 
        default=30,
        help="Number of days of historical data to fetch"
    )
    parser.add_argument(
        "--action",
        type=str,
        choices=["prices", "metrics", "news", "insider", "market-cap", "all"],
        default="prices",
        help="Type of data to fetch"
    )
    
    return parser.parse_args()


def main():
    """Main function."""
    args = parse_args()
    
    # Set the API provider if specified
    if args.api_provider:
        set_api_provider(args.api_provider)
    
    # Get the current provider for display
    current_provider = get_current_provider()
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=args.days)
    end_date_str = format_date(end_date)
    start_date_str = format_date(start_date)
    
    print(f"\n{'='*80}")
    print(f"API Provider Demo - Using: {current_provider}")
    print(f"{'='*80}")
    print(f"Ticker: {args.ticker}")
    print(f"Date Range: {start_date_str} to {end_date_str}")
    print(f"{'='*80}\n")
    
    # Fetch data based on the specified action
    if args.action in ["prices", "all"]:
        print(f"\n{'='*40}")
        print(f"PRICE DATA")
        print(f"{'='*40}")
        try:
            prices = get_prices(args.ticker, start_date_str, end_date_str)
            if prices:
                df = pd.DataFrame([p.model_dump() for p in prices])
                print(f"Found {len(prices)} price records")
                print(df.head().to_string())
            else:
                print("No price data found")
        except Exception as e:
            print(f"Error fetching price data: {e}")
    
    if args.action in ["metrics", "all"]:
        print(f"\n{'='*40}")
        print(f"FINANCIAL METRICS")
        print(f"{'='*40}")
        try:
            metrics = get_financial_metrics(args.ticker, end_date_str)
            if metrics:
                print(f"Found {len(metrics)} financial metrics records")
                for metric in metrics[:2]:  # Show only first 2 for brevity
                    print(f"Report Period: {metric.report_period}")
                    print(f"Revenue: {metric.revenue}")
                    print(f"Net Income: {metric.net_income}")
                    print(f"EPS: {metric.eps}")
                    print(f"Market Cap: {metric.market_cap}")
                    print("-" * 30)
            else:
                print("No financial metrics found")
        except Exception as e:
            print(f"Error fetching financial metrics: {e}")
    
    if args.action in ["news", "all"]:
        print(f"\n{'='*40}")
        print(f"COMPANY NEWS")
        print(f"{'='*40}")
        try:
            news = get_company_news(args.ticker, end_date_str, start_date_str, limit=5)
            if news:
                print(f"Found {len(news)} news items")
                for item in news[:3]:  # Show only first 3 for brevity
                    print(f"Date: {item.date}")
                    print(f"Title: {item.title}")
                    print(f"Source: {item.source}")
                    print("-" * 30)
            else:
                print("No news found")
        except Exception as e:
            print(f"Error fetching company news: {e}")
    
    if args.action in ["insider", "all"]:
        print(f"\n{'='*40}")
        print(f"INSIDER TRADES")
        print(f"{'='*40}")
        try:
            trades = get_insider_trades(args.ticker, end_date_str, start_date_str, limit=5)
            if trades:
                print(f"Found {len(trades)} insider trades")
                for trade in trades[:3]:  # Show only first 3 for brevity
                    print(f"Filing Date: {trade.filing_date}")
                    print(f"Insider Name: {trade.insider_name}")
                    print(f"Transaction Type: {trade.transaction_type}")
                    print(f"Shares: {trade.shares}")
                    print(f"Price: {trade.price}")
                    print("-" * 30)
            else:
                print("No insider trades found")
        except Exception as e:
            print(f"Error fetching insider trades: {e}")
    
    if args.action in ["market-cap", "all"]:
        print(f"\n{'='*40}")
        print(f"MARKET CAP")
        print(f"{'='*40}")
        try:
            market_cap = get_market_cap(args.ticker, end_date_str)
            if market_cap:
                print(f"Market Cap: ${market_cap:,.2f}")
            else:
                print("No market cap data found")
        except Exception as e:
            print(f"Error fetching market cap: {e}")
    
    print(f"\n{'='*80}")
    print("Demo completed")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
