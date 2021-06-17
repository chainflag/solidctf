#!/usr/bin/python3

import pytest


@pytest.fixture(scope="module")
def metaCoinInstance(ConvertLib, MetaCoin, module_isolation, accounts):
    ConvertLib.deploy({'from': accounts[0]})
    m = MetaCoin.deploy({'from': accounts[0]})
    yield m


def test_initial_balance(metaCoinInstance, accounts):
    '''should put 10000 MetaCoin in the first account'''
    assert metaCoinInstance.getBalance(accounts[0]) == 10000, "10000 wasn't in the first account"


def test_library_fn(metaCoinInstance, accounts):
    '''should call a function that depends on a linked library'''
    metaCoinBalance = metaCoinInstance.getBalance(accounts[0])
    metaCoinEthBalance = metaCoinInstance.getBalanceInEth(accounts[0])

    assert metaCoinEthBalance == 2 * metaCoinBalance, "Library function returned unexpected function, linkage may be broken"


def test_transfer(metaCoinInstance, accounts):
    '''should send coin correctly'''
    # Get initial balances of first and second account.
    accountOneStartingBalance = metaCoinInstance.getBalance(accounts[0])
    accountTwoStartingBalance = metaCoinInstance.getBalance(accounts[1])

    # Make transaction from first account to second.
    amount = 10
    metaCoinInstance.sendCoin(accounts[1], amount, {'from': accounts[0]})

    # Get balances of first and second account after the transactions.
    accountOneEndingBalance = metaCoinInstance.getBalance(accounts[0])
    accountTwoEndingBalance = metaCoinInstance.getBalance(accounts[1])

    assert accountOneEndingBalance == accountOneStartingBalance - amount, "Amount wasn't correctly taken from the sender"
    assert accountTwoEndingBalance == accountTwoStartingBalance + amount, "Amount wasn't correctly sent to the receiver"
