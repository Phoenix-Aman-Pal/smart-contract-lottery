import imp, time
from multiprocessing.spawn import import_main_path
from brownie import accounts, Lottery, config, network
from scripts.helpful_scripts import get_account, get_contract, fund_with_link


def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from":account}, publish_source = config["networks"][network.show_active()].get("verify", False),
    )
    return lottery
    print("Deployed Lottery !!!")

def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_txn = lottery.startLottery({"from": account})
    starting_txn.wait(1)
    print("Lottery started !!!")

def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 10**8
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("You Entered the lottery !!!")

def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # Fund the contract then end the lottery
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    ending_transaction = lottery.endLottery({"from": account})
    ending_transaction.wait(1)
    time.sleep(60) # Because after the end lottery chainink with call fulfilness so we need some time for it
    print(f"{lottery.recentWinner()} is new winner !!!")

def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
