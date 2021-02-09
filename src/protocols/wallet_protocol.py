from dataclasses import dataclass
from typing import List, Tuple, Optional

from src.types.coin import Coin
from src.types.program import Program
from src.types.spend_bundle import SpendBundle
from src.types.header_block import HeaderBlock
from src.types.sized_bytes import bytes32
from src.util.ints import uint32, uint128, uint8
from src.util.streamable import Streamable, streamable

"""
Protocol between wallet (SPV node) and full node.
Note: When changing this file, also change protocol_message_types.py, and the protocol version in shared_protocol.py
"""


@dataclass(frozen=True)
@streamable
class RequestPuzzleSolution(Streamable):
    coin_name: bytes32
    sub_height: uint32


@dataclass(frozen=True)
@streamable
class PuzzleSolutionResponse(Streamable):
    coin_name: bytes32
    sub_height: uint32
    puzzle: Program
    solution: Program


@dataclass(frozen=True)
@streamable
class RespondPuzzleSolution(Streamable):
    response: PuzzleSolutionResponse


@dataclass(frozen=True)
@streamable
class RejectPuzzleSolution(Streamable):
    coin_name: bytes32
    sub_height: uint32


@dataclass(frozen=True)
@streamable
class SendTransaction(Streamable):
    transaction: SpendBundle


@dataclass(frozen=True)
@streamable
class TransactionAck(Streamable):
    txid: bytes32
    status: uint8  # MempoolInclusionStatus
    error: Optional[str]


@dataclass(frozen=True)
@streamable
class NewPeakWallet(Streamable):
    header_hash: bytes32
    sub_block_height: uint32
    weight: uint128
    fork_point_with_previous_peak: uint32


@dataclass(frozen=True)
@streamable
class RequestSubBlockHeader(Streamable):
    sub_height: uint32


@dataclass(frozen=True)
@streamable
class RespondSubBlockHeader(Streamable):
    header_block: HeaderBlock


@dataclass(frozen=True)
@streamable
class RejectHeaderRequest(Streamable):
    height: uint32


@dataclass(frozen=True)
@streamable
class RequestRemovals(Streamable):
    sub_height: uint32
    header_hash: bytes32
    coin_names: Optional[List[bytes32]]


@dataclass(frozen=True)
@streamable
class RespondRemovals(Streamable):
    sub_height: uint32
    header_hash: bytes32
    coins: List[Tuple[bytes32, Optional[Coin]]]
    proofs: Optional[List[Tuple[bytes32, bytes]]]


@dataclass(frozen=True)
@streamable
class RejectRemovalsRequest(Streamable):
    sub_height: uint32
    header_hash: bytes32


@dataclass(frozen=True)
@streamable
class RequestAdditions(Streamable):
    sub_height: uint32
    header_hash: bytes32
    puzzle_hashes: Optional[List[bytes32]]


@dataclass(frozen=True)
@streamable
class RespondAdditions(Streamable):
    sub_height: uint32
    header_hash: bytes32
    coins: List[Tuple[bytes32, List[Coin]]]
    proofs: Optional[List[Tuple[bytes32, bytes, Optional[bytes]]]]


@dataclass(frozen=True)
@streamable
class RejectAdditionsRequest(Streamable):
    sub_height: uint32
    header_hash: bytes32


@dataclass(frozen=True)
@streamable
class RequestHeaderBlocks(Streamable):
    start_sub_height: uint32
    end_sub_height: uint32


@dataclass(frozen=True)
@streamable
class RejectHeaderBlocks(Streamable):
    start_sub_height: uint32
    end_sub_height: uint32


@dataclass(frozen=True)
@streamable
class RespondHeaderBlocks(Streamable):
    start_sub_height: uint32
    end_sub_height: uint32
    header_blocks: List[HeaderBlock]
