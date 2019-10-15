from desktop.lib.models.account import Account


def get_key_for_account(account: Account) -> str:
    return get_key_for_endpoint(account.endpoint)


def get_key_for_endpoint(endpoint: str) -> str:
    return f"GitHub - {endpoint}"
