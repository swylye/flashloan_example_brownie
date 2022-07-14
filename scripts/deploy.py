from brownie import network, config, accounts, Contract, interface, FlashLoan
from scripts.helpful_scripts import get_account


def main():
    if network.show_active() == "polygon-main-fork":
        account = accounts.at(
            config["networks"][network.show_active()]["dai_whale_address"], force=True
        )
    else:
        account = get_account()
    flashloan = deploy_flash_loan(account)


def deploy_flash_loan(account):
    flashloan = FlashLoan.deploy(
        config["networks"][network.show_active()]["dai_pool_address"],
        {"from": account},
    )
    return flashloan
