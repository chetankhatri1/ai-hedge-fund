# API Provider System

This module provides a flexible system for switching between different financial data API providers in the AI Hedge Fund application.

## Overview

The API provider system allows the application to fetch financial data from multiple sources, providing flexibility and redundancy. Currently, the system supports the following providers:

- **Financial Datasets API**: The primary data provider with comprehensive financial data
- **Yahoo Finance API**: An alternative data provider for backup or comparison

## Architecture

The system is built around the following components:

1. **BaseAPIProvider** (`base.py`): An abstract base class that defines the interface all API providers must implement
2. **FinancialDatasetsProvider** (`financial_datasets.py`): Implementation for the Financial Datasets API
3. **YahooFinanceProvider** (`yahoo_finance.py`): Implementation for the Yahoo Finance API
4. **APIProviderManager** (`provider_manager.py`): A manager class that handles provider selection and switching

## Usage

### Basic Usage

```python
from tools.api import get_prices, set_api_provider

# Use the default provider (determined by available API keys)
prices = get_prices("AAPL", "2025-01-01", "2025-01-31")

# Switch to Yahoo Finance API
set_api_provider("yahoo_finance")
prices = get_prices("AAPL", "2025-01-01", "2025-01-31")

# Switch back to Financial Datasets API
set_api_provider("financial_datasets")
prices = get_prices("AAPL", "2025-01-01", "2025-01-31")
```

### Command-line Arguments

The system includes support for command-line arguments to specify the API provider:

```python
from tools.api import parse_api_provider_args

# Parse command-line arguments and set the provider if specified
args = parse_api_provider_args()
```

This allows scripts to accept an `--api-provider` argument:

```bash
python3 my_script.py --api-provider yahoo_finance
```

### Available Providers

To get a list of available providers:

```python
from tools.api import get_available_providers

providers = get_available_providers()
print(providers)  # {'financial_datasets': 'Financial Datasets API', 'yahoo_finance': 'Yahoo Finance API'}
```

### Current Provider

To check which provider is currently active:

```python
from tools.api import get_current_provider

current = get_current_provider()
print(current)  # 'financial_datasets'
```

## Environment Variables

The system requires API keys to be set in environment variables:

- `FINANCIAL_DATASETS_API_KEY`: API key for Financial Datasets API
- `YAHOO_FINANCE_API_KEY`: API key for Yahoo Finance API

## Demo Script

A demo script is provided to showcase the API provider switching functionality:

```bash
python3 src/api_provider_demo.py --action all --ticker AAPL
python3 src/api_provider_demo.py --action prices --ticker MSFT --api-provider yahoo_finance
```

## Extending the System

To add a new API provider:

1. Create a new provider class that inherits from `BaseAPIProvider`
2. Implement all required methods
3. Add the provider to the `_providers` dictionary in `APIProviderManager`

Example:

```python
# new_provider.py
from .base import BaseAPIProvider

class NewProvider(BaseAPIProvider):
    """Implementation for a new API provider."""
    
    @property
    def name(self) -> str:
        return "New API Provider"
    
    # Implement all required methods...

# provider_manager.py
from .new_provider import NewProvider

class APIProviderManager:
    # ...
    _providers: Dict[str, Type[BaseAPIProvider]] = {
        "financial_datasets": FinancialDatasetsProvider,
        "yahoo_finance": YahooFinanceProvider,
        "new_provider": NewProvider,
    }
    # ...
```
