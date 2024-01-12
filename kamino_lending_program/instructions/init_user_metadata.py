from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.sysvar import RENT
from solders.instruction import Instruction, AccountMeta
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class InitUserMetadataArgs(typing.TypedDict):
    referrer: Pubkey
    user_lookup_table: Pubkey


layout = borsh.CStruct("referrer" / BorshPubkey, "user_lookup_table" / BorshPubkey)


class InitUserMetadataAccounts(typing.TypedDict):
    owner: Pubkey
    user_metadata: Pubkey


def init_user_metadata(
    args: InitUserMetadataArgs,
    accounts: InitUserMetadataAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["owner"], is_signer=True, is_writable=True),
        AccountMeta(
            pubkey=accounts["user_metadata"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=RENT, is_signer=False, is_writable=False),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"u\xa9\xb0E\xc5\x17\x0f\xa2"
    encoded_args = layout.build(
        {
            "referrer": args["referrer"],
            "user_lookup_table": args["user_lookup_table"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
