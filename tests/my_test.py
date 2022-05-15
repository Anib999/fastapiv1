import pytest
from app.calculation import add, BankAccount

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    print('50 default amount')
    return BankAccount(50)

# @pytest.mark.parametrize("num1, num2, result",[
#     (3, 4, 7),
#     (9, 10, 18)
# ])
# def test_add(num1, num2, result):
#     print('testing add function')
#     assert add(num1, num2) == result

def test_first_deposit(bank_account):
    # bank_account = BankAccount(5000)
    assert bank_account.balance == 50

def test_withdraw():
    bank_account = BankAccount(50)
    bank_account.withdraw(50)
    assert bank_account.balance == 0

def test_withdraw():
    bank_account = BankAccount(50)
    bank_account.deposit(50)
    assert bank_account.balance == 100

def test_interest():
    bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55

def test_bank_trans(zero_bank_account):
    zero_bank_account.deposit(200)
    zero_bank_account.withdraw(100)
    assert zero_bank_account.balance == 100

def test_insufficient(zero_bank_account):
    with pytest.raises(Exception):
        zero_bank_account.withdraw(100)