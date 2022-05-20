import json
from pytest import console_main
from web3 import Web3
import os
from dotenv import load_dotenv
from brownie import EthPool, network, config, Contract
from scripts.utils_scripts import (
    get_account,
    get_b_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)

WEI_ETH = 1000000000000000000
abi = json.loads(
    '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"depositRewards","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"depositToPool","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"deposits","outputs":[{"internalType":"uint256","name":"epoch","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"rewards","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"poolWeight","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalOfAccount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"withdrawAmount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"withdrawAll","outputs":[],"stateMutability":"payable","type":"function"}]'
)
address = "0x9f2bf94D87A2fE4F07AC391bb1AEb73630E5524f"
eth_pool = Contract.from_abi("EthPool", address, abi)

accounts = []


def deposit_to_pool():
    tx = eth_pool.depositToPool(
        {"from": get_b_account(), "value": WEI_ETH * 0.1, "priority_fee": 35000000000}
    )
    tx.wait(1)


def depositRewards():
    tx = eth_pool.depositToPool(
        {"from": get_account(), "value": WEI_ETH * 0.1, "priority_fee": 35000000000}
    )
    tx.wait(1)


def total_account_b():
    total = eth_pool.totalOfAccount({"from": get_b_account()})
    print(total)


def total_account():
    total = eth_pool.totalOfAccount({"from": get_account()})
    print(total)


def withdraw_all_b():
    tx = eth_pool.withdraw({"from": get_b_account()})
    tx.wait(1)


def withdraw_all():
    tx = eth_pool.withdraw({"from": get_account()})
    tx.wait(1)


def main():
    # deposit_to_pool()
    total_account()
    total_account_b()
