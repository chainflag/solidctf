#!/usr/bin/python3

import pytest


@pytest.fixture(scope="module")
def greeter_instance(Greeter, accounts):
    m = Greeter.deploy("HelloWorld", {'from': accounts[0]})
    yield m


def test_initial_greeting(greeter_instance):
    assert greeter_instance.greet() == "HelloWorld"


def test_set_greeting(greeter_instance, accounts):
    greeter_instance.setGreeting("HelloChainFlag", {'from': accounts[0]})
    assert greeter_instance.greet() == "HelloChainFlag"
