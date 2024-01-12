from solana.rpc.api import Client
from solders.rpc.responses import GetAccountInfoResp
from kamino_lending_program.program_id import PROGRAM_ID
from kamino_lending_program.accounts import (
    Reserve,
)
from solders.pubkey import Pubkey
from spl.token.client import Token
from spl.token.constants import TOKEN_PROGRAM_ID


JLP = '27G8MtK7VtTcCHkpASjSDdkWWYfoqT6ggEuKidVJidD4'  # decimal:6


def get_account(client: Client, address: str) -> GetAccountInfoResp:
    return client.get_account_info(Pubkey.from_string(address))


def get_account_as_reserve(client: Client, address: str) -> Reserve:
    acc = get_account(client, address)
    return Reserve.decode(acc.value.data)


def get_token_balance(client: Client, token_address: str, owner: str):
    tk = Token(client, Pubkey.from_string(
        token_address), TOKEN_PROGRAM_ID, None)
    return int(tk.get_balance(Pubkey.from_string(owner)).value.amount)


def main():
    headers = {
        'Origin': 'https://app.kamino.finance',
        'Solana-Client': 'js/0.0.0-development',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    client = Client(
        'https://hubblep-main-0776.mainnet.rpcpool.com/', extra_headers=headers)
    # jlp reserve
    reserve = get_account_as_reserve(
        client, 'EAA3VVsxUuQB1Tm5x7TJkq9ATtiX5Qwq8ok7gXwim7oo')

    # jlp decimals: 6
    deposit_max = reserve.config.deposit_limit

    # vault
    vault = str(reserve.liquidity.supply_vault)
    balance = get_token_balance(client, JLP, vault)

    remain_size = deposit_max - balance
    print('JLP枠残り:', remain_size/10**6)


if __name__ == '__main__':
    main()
