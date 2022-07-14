from brownie import network, config, accounts, Contract, interface, FlashLoan
from scripts.helpful_scripts import get_account
from scripts.deploy import deploy_flash_loan
import pytest


def test_flashloan():
    if network.show_active() != "polygon-main-fork":
        pytest.skip()
    account = accounts.at(
        config["networks"][network.show_active()]["dai_whale_address"], force=True
    )
    # deploy contract
    flashloan = deploy_flash_loan(account)
    # transfer DAI to contract
    dai_address = config["networks"][network.show_active()]["dai_token_address"]
    transfer_amount = 2000 * 10**18
    dai_token = interface.IERC20(dai_address)
    transfer_tx = dai_token.transfer(
        flashloan.address, transfer_amount, {"from": account}
    )
    transfer_tx.wait(1)
    initial_balance = dai_token.balanceOf(flashloan.address)
    # get flash loan
    loan_amount = 1500 * 10**18
    flashloan_tx = flashloan.createFlashLoan(
        dai_address, loan_amount, {"from": account}
    )
    flashloan_tx.wait(1)
    new_balance = dai_token.balanceOf(flashloan.address)
    assert new_balance < initial_balance
