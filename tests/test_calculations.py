from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds
import pytest

@pytest.fixture
def zero_bank_account():
    print("call fix ture 0")
    return BankAccount()

@pytest.fixture
def bank_account():
    print("call fix ture")
    return BankAccount(50)

@pytest.mark.parametrize("num1,num2,expected",[
    (1,2,3),
    (2,3,5),
    (4,5,9)
])


def test_add(num1,num2,expected):
    print("------>testing add function<---------")
    assert add(num1,num2) == expected
    

def test_subtract():
    print("------>testing subtract function<---------")
    assert subtract(2,2) == 0
    

def test_multiply():
    print("------>testing multiply function<---------")
    assert multiply(2,2) == 4
    


def test_divide():
    print("------>testing divide function<---------")
    assert divide(2,2) == 1
    
def test_bank_set_initial_amount(bank_account):
    print("---------->test_bank_set_initial_amount<------------")
    assert bank_account.balance == 50
    
def test_withdraw(bank_account):
    print("---------->test_withdraw<-----------")
    bank_account.withdraw(10)
    assert bank_account.balance == 40
    
def test_deposit(bank_account):
    print("---------->test_deposit<-----------")
    bank_account.deposit(10)
    assert bank_account.balance == 60
    
def test_interest(bank_account):
    print("---------->test_interest<-----------")
    bank_account.collect_interest()
    assert round(bank_account.balance,6) == 55
    
@pytest.mark.parametrize("deposit,withdraw,expected",[
    (100,50,50),
    (50,20,30),
])
def test_bank_transaction(zero_bank_account,deposit,withdraw,expected):
    print("---------->test_bank_transaction<-----------")
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected
    
def test_insufficient_funds(zero_bank_account):
    with pytest.raises(InsufficientFunds):
        zero_bank_account.withdraw(50)
