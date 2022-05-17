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

# A, B, C, D users
# O is owner account
# sequence:
# A deposit 8 eth
# B deposit 1 eth
# C deposit 1 eth
# O rewards 5 eth
# A deposit 10 eth
# D deposit 10 eth
# O rewards 10 eth
# A withdraw 10 eth
# O rewards 10 eth
def test_complex_sequence():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local enviroments")
    ownerAccount = get_account()
    accountA = getAccountOfIndex(1)
    accountB = getAccountOfIndex(2)
    accountC = getAccountOfIndex(3)
    accountD = getAccountOfIndex(4)
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
    tx5 = eth_pool.depositToPool({"from": accountA, "value": WEI_ETH * 5})
    tx5.wait(1)
    tx6 = eth_pool.depositToPool({"from": accountD, "value": WEI_ETH * 10})
    tx6.wait(1)
    tx7 = eth_pool.depositRewards({"from": ownerAccount, "value": WEI_ETH * 10})
    tx7.wait(1)
    assert eth_pool.totalOfAccount({"from": ownerAccount}) == 0
    assert eth_pool.totalOfAccount({"from": accountA}) > WEI_ETH * 22.6666
    assert eth_pool.totalOfAccount({"from": accountA}) < WEI_ETH * 22.6667
    assert eth_pool.totalOfAccount({"from": accountB}) == WEI_ETH * 2
    assert eth_pool.totalOfAccount({"from": accountC}) == WEI_ETH * 2
    assert eth_pool.totalOfAccount({"from": accountD}) > WEI_ETH * 13.3333
    assert eth_pool.totalOfAccount({"from": accountD}) < WEI_ETH * 13.3334
    tx8 = eth_pool.withdraw(WEI_ETH * 10, {"from": accountA})
    tx8.wait(1)
    tx9 = eth_pool.depositRewards({"from": ownerAccount, "value": WEI_ETH * 10})
    tx9.wait(1)
    assert eth_pool.totalOfAccount({"from": accountA}) > WEI_ETH * 16.8888
    assert eth_pool.totalOfAccount({"from": accountA}) < WEI_ETH * 16.8889
    assert eth_pool.totalOfAccount({"from": accountB}) > WEI_ETH * 2.6666
    assert eth_pool.totalOfAccount({"from": accountB}) < WEI_ETH * 2.6667
    assert eth_pool.totalOfAccount({"from": accountC}) > WEI_ETH * 2.6666
    assert eth_pool.totalOfAccount({"from": accountC}) < WEI_ETH * 2.6667
    assert eth_pool.totalOfAccount({"from": accountD}) > WEI_ETH * 17.7777
    assert eth_pool.totalOfAccount({"from": accountD}) < WEI_ETH * 17.7778


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
    tx3 = eth_pool.withdrawAll({"from": accountA})
    tx3.wait(1)
    balanceAfter = accountA.balance()
    assert eth_pool.totalOfAccount({"from": accountA}) == 0
    assert (balanceBefore + (WEI_ETH * 13)) == balanceAfter


def test_partial_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local enviroments")
    ownerAccount = get_account()
    accountA = getAccountOfIndex(1)
    accountB = getAccountOfIndex(2)
    eth_pool = deploy_eth_pool()
    tx = eth_pool.depositToPool({"from": accountA, "value": WEI_ETH * 10})
    tx.wait(1)
    tx2 = eth_pool.depositToPool({"from": accountB, "value": WEI_ETH * 5})
    tx2.wait(1)
    tx3 = eth_pool.depositRewards({"from": ownerAccount, "value": WEI_ETH * 3})
    tx3.wait(1)
    assert eth_pool.totalOfAccount({"from": accountA}) == WEI_ETH * 12
    assert eth_pool.totalOfAccount({"from": accountB}) == WEI_ETH * 6
    tx4 = eth_pool.withdraw(WEI_ETH * 6, {"from": accountA})
    tx4.wait(1)
    tx5 = eth_pool.depositRewards({"from": ownerAccount, "value": WEI_ETH * 8})
    tx5.wait(1)
    assert eth_pool.totalOfAccount({"from": accountA}) == WEI_ETH * 10
    assert eth_pool.totalOfAccount({"from": accountB}) == WEI_ETH * 10


def main():
    test_withdraw_all()
    test_only_owner_can_deposits_rewards()
    test_partial_withdraw()
    test_complex_sequence()
