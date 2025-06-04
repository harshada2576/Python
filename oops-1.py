from abc import ABC, abstractmethod

# Abstract Class - Demonstrating Abstraction
class Account(ABC):

    def __init__(self, owner, balance=0):
        self._owner = owner              # Protected attribute
        self.__balance = balance         # Private attribute (Encapsulation)

    @abstractmethod
    def account_type(self):
        pass

    # Getter method for balance - part of Encapsulation
    def get_balance(self):
        return self.__balance

    # Setter method for deposit - with validation
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"Deposited ${amount} to {self._owner}'s account.")
        else:
            print("Invalid deposit amount.")

    # Setter method for withdrawal - with validation
    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            print(f"Withdrew ${amount} from {self._owner}'s account.")
        else:
            print("Insufficient funds or invalid amount.")

# Subclass - implements abstraction
class SavingsAccount(Account):

    def account_type(self):
        return "Savings Account"

# Subclass - implements abstraction
class CheckingAccount(Account):

    def account_type(self):
        return "Checking Account"

# Test Program
def main():
    acc1 = SavingsAccount("Alice", 1000)
    acc2 = CheckingAccount("Bob", 500)

    print(f"{acc1._owner} has a {acc1.account_type()} with balance: ${acc1.get_balance()}")
    acc1.deposit(200)
    acc1.withdraw(100)
    print(f"Updated balance: ${acc1.get_balance()}")

    print(f"\n{acc2._owner} has a {acc2.account_type()} with balance: ${acc2.get_balance()}")
    acc2.withdraw(600)  # This should fail due to insufficient funds

if __name__ == "__main__":
    main()
