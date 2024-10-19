import unittest
class BankAccount:
    def __init__(self, account_holder, initial_balance=0):
        """Инициализация банковского счета."""
        self.account_holder = account_holder
        self.balance = initial_balance
    def deposit(self, amount):
        """Внесение денег на счет."""
        if amount <= 0:
            return "Сумма вклада должна быть положительной."
        self.balance += amount
        return self.balance
    def withdraw(self, amount):
        """Снятие денег со счета."""
        if amount <= 0:
            return "Сумма снятия должна быть положительной."
        if amount > self.balance:
            return "Недостаточно средств на счете."
        self.balance -= amount
        return self.balance
    def get_balance(self):
        """Получение текущего баланса."""
        return self.balance

class TestBank(unittest.TestCase):
    def test_TestBank(self):
        bank = BankAccount("Sun", 100)
        self.assertTrue(bank.balance >= 0)
    def test_deposit(self):
        bank = BankAccount("Sun", 100)
        res = bank.deposit(1)
        self.assertTrue(res >= 0)
    def test_deposit_counter(self):
        bank = BankAccount("Sun", 0)
        bank.deposit(1)
        bank.deposit(1)
        bank.deposit(1)
        self.assertEqual(bank.balance, 3)
    def test_withdraw(self):
        bank = BankAccount("Sun", 100)
        res = bank.withdraw(1)
        self.assertTrue(res >= 0)
    def test_withdraw_balans(self):
        bank = BankAccount("Sun", 100)
        res = bank.withdraw(90)
        self.assertTrue(res >= bank.balance)
    def test_get_balance(self):
        bank = BankAccount("Sun", 0)
        bank.deposit(1)
        bank.withdraw(1)
        self.assertEqual(bank.balance, 0)

if __name__ == "__main__":
    unittest.main()