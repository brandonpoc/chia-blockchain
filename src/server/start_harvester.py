import pathlib

from typing import Dict

from src.consensus.constants import ConsensusConstants
from src.consensus.default_constants import DEFAULT_CONSTANTS
from src.harvester.harvester import Harvester
from src.harvester.harvester_api import HarvesterAPI
from src.server.outbound_message import NodeType
from src.types.peer_info import PeerInfo
from src.types.sized_bytes import bytes32
from src.util.config import load_config_cli
from src.util.default_root import DEFAULT_ROOT_PATH
from src.rpc.harvester_rpc_api import HarvesterRpcApi

from src.server.start_service import run_service

# See: https://bugs.python.org/issue29288
"".encode("idna")

SERVICE_NAME = "harvester"


def service_kwargs_for_harvester(
    root_path: pathlib.Path,
    config: Dict,
    consensus_constants: ConsensusConstants,
) -> Dict:
    connect_peers = [PeerInfo(config["farmer_peer"]["host"], config["farmer_peer"]["port"])]

    genesis_challenge = bytes32(bytes.fromhex(config["network_genesis_challenges"][config["selected_network"]]))
    harvester = Harvester(root_path, config, consensus_constants.replace(GENESIS_CHALLENGE=genesis_challenge))
    peer_api = HarvesterAPI(harvester)

    kwargs = dict(
        root_path=root_path,
        node=harvester,
        peer_api=peer_api,
        node_type=NodeType.HARVESTER,
        advertised_port=config["port"],
        service_name=SERVICE_NAME,
        server_listen_ports=[config["port"]],
        connect_peers=connect_peers,
        auth_connect_peers=True,
        network_id=genesis_challenge,
    )
    if config["start_rpc_server"]:
        kwargs["rpc_info"] = (HarvesterRpcApi, config["rpc_port"])
    return kwargs


def main():
    config = load_config_cli(DEFAULT_ROOT_PATH, "config.yaml", SERVICE_NAME)
    kwargs = service_kwargs_for_harvester(DEFAULT_ROOT_PATH, config, DEFAULT_CONSTANTS)
    return run_service(**kwargs)


if __name__ == "__main__":
    main()
