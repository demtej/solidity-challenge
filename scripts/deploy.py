from brownie import EthPool, network, config
from web3 import Web3
from scripts.utils_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_eth_pool():
    account = get_account()
    eth_pool = EthPool.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {eth_pool.address}")
    return eth_pool


def main():
    deploy_eth_pool()
