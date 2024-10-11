import os
import uuid
from typing import List, Dict, Any

import requests

__all__ = [
    "get_accounts",
    "get_balance",
    "get_pots",
    "deposit_into_pot",
    "withdraw_from_pot",
]

API_BASE_URL = "https://api.monzo.com"


class MonzoAPIError(Exception):
    """Custom exception for Monzo API errors."""

    pass


def _get_access_token() -> str:
    """Retrieve the Monzo access token from environment variables."""
    access_token = os.getenv("MONZO_ACCESS_TOKEN")
    if not access_token:
        raise ValueError("MONZO_ACCESS_TOKEN not found in environment variables")
    return access_token


def _make_request(method: str, endpoint: str, **kwargs: Any) -> Dict[str, Any]:
    """Make a request to the Monzo API."""
    headers = {
        "Authorization": f"Bearer {_get_access_token()}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    url = f"{API_BASE_URL}/{endpoint}"
    response = requests.request(method, url, headers=headers, **kwargs)

    if response.status_code == 200:
        return response.json()
    else:
        raise MonzoAPIError(f"API request failed: {response.status_code} - {response.text}")


def get_accounts() -> List[Dict[str, Any]]:
    """Retrieves a list of accounts from the Monzo API."""
    data = _make_request("GET", "accounts")
    return data.get("accounts", [])


def get_balance(account_id: str) -> Dict[str, Any]:
    """Retrieves the balance for a specific Monzo account."""
    return _make_request("GET", f"balance?account_id={account_id}")


def get_pots(account_id: str) -> List[Dict[str, Any]]:
    """Retrieves a list of all pots for a specific Monzo account."""
    data = _make_request("GET", f"pots?current_account_id={account_id}")
    return data.get("pots", [])


def deposit_into_pot(source_account_id: str, pot_id: str, amount: int, dedupe_id: str = None) -> Dict[str, Any]:
    """Deposits money into a specified pot from the main account."""
    data = {
        "source_account_id": source_account_id,
        "amount": str(amount),
        "dedupe_id": dedupe_id or str(uuid.uuid4()),
    }
    return _make_request("PUT", f"pots/{pot_id}/deposit", data=data)


def withdraw_from_pot(destination_account_id: str, pot_id: str, amount: int, dedupe_id: str = None) -> Dict[str, Any]:
    """Withdraws money from a specified pot to the main account."""
    data = {
        "destination_account_id": destination_account_id,
        "amount": str(amount),
        "dedupe_id": dedupe_id or str(uuid.uuid4()),
    }
    return _make_request("PUT", f"pots/{pot_id}/withdraw", data=data)
