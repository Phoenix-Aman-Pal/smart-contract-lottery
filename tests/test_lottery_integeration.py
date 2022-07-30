import imp
from re import I
from eth_account import Account
from scripts.deploy import deploy_lottery
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, fund_with_link, get_account
from brownie import network
import pytest
import time


def test_choose_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    time.sleep(180)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0

# from scripts.helpful_scripts import (
#     get_account,
#     fund_with_link,
#     LOCAL_BLOCKCHAIN_ENVIRONMENTS,
# )
# import time
# from brownie import network
# import pytest


# def test_can_pick_winner(lottery_contract):
#     if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
#         pytest.skip()

#     account = get_account()
#     lottery_contract.startLottery({"from": account})
#     lottery_contract.enter(
#         {"from": account, "value": lottery_contract.getEntranceFee()}
#     )
#     lottery_contract.enter(
#         {"from": account, "value": lottery_contract.getEntranceFee()}
#     )
#     fund_with_link(lottery_contract)
#     lottery_contract.endLottery({"from": account})
#     time.sleep(180)
#     assert lottery_contract.recentWinner() == account
#     assert lottery_contract.balance() == 0