from os import access
import pytest
from brownie import accounts, network, exceptions
from scripts.utils_scripts import (
    get_account,
    getAccountOfIndex,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from scripts.deploy import deploy_eth_pool

WEI_ETH = 1000000000000000000


def test_sequence():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local enviroments")
    ownerAccount = get_account()
    accountA = getAccountOfIndex(1)
    accountB = getAccountOfIndex(2)
    accountC = getAccountOfIndex(3)
    eth_pool = deploy_eth_pool()
    tx = eth_pool.depositToPool({"from": accountA, "value": WEI_ETH * 8})
    tx.wait(1)
    tx2 = eth_pool.depositToPool({"from": accountB, "value": WEI_ETH * 1})
    tx2.wait(1)
    tx3 = eth_pool.depositToPool({"from": accountC, "value": WEI_ETH * 1})
    tx3.wait(1)
    assert eth_pool.totalOfAccount({"from": accountA}) == WEI_ETH * 8
    assert eth_pool.totalOfAccount({"from": accountB}) == WEI_ETH * 1
    assert eth_pool.totalOfAccount({"from": accountC}) == WEI_ETH * 1
    tx4 = eth_pool.depositRewards({"from": ownerAccount, "value": WEI_ETH * 5})
    tx4.wait(1)
    assert eth_pool.totalOfAccount({"from": ownerAccount}) == 0
    assert eth_pool.totalOfAccount({"from": accountA}) == WEI_ETH * 12.00
    assert eth_pool.totalOfAccount({"from": accountB}) == WEI_ETH * 1.50
    assert eth_pool.totalOfAccount({"from": accountC}) == WEI_ETH * 1.50


def test_only_owner_can_deposits_rewards():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local enviroments")
    eth_pool = deploy_eth_pool()
    bad_actor = getAccountOfIndex(1)
    with pytest.raises(exceptions.VirtualMachineError):
        eth_pool.depositRewards({"from": bad_actor, "value": WEI_ETH * 5})


def test_withdraw_all():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local enviroments")
    ownerAccount = get_account()
    accountA = getAccountOfIndex(1)
    eth_pool = deploy_eth_pool()
    tx = eth_pool.depositToPool({"from": accountA, "value": WEI_ETH * 8})
    tx.wait(1)
    assert eth_pool.totalOfAccount({"from": accountA}) == WEI_ETH * 8
    tx2 = eth_pool.depositRewards({"from": ownerAccount, "value": WEI_ETH * 5})
    tx2.wait(1)
    balanceBefore = accountA.balance()
    tx3 = eth_pool.withdraw({"from": accountA})
    tx3.wait(1)
    balanceAfter = accountA.balance()
    assert eth_pool.totalOfAccount({"from": accountA}) == 0
    assert (balanceBefore + (WEI_ETH * 13)) == balanceAfter


def main():
    test_withdraw_all()
    test_only_owner_can_deposits_rewards()
    test_sequence()
