# ============================================== Case Study 02 =========================================================
# ===================================== 'SafeBank' Online Banking System ===============================================
# *********************************************** E. Thompson **********************************************************
"""
Case Study Story:
In the digital age, online banking has become the norm.
SafeBank, a leading financial institution, is looking to revamp its online banking
interface to ensure it's not only user-friendly but also robust against potential
errors and misuse.

The new system should allow users to perform common banking operations like
checking balances, transferring funds between accounts, and depositing or
withdrawing money. However, with the convenience of online banking comes the
responsibility of ensuring transactions are error-free and secure. For instance, a
user shouldn't be able to transfer negative amounts or over-withdraw beyond
their account balance.

Students are tasked with designing this new interface. They must implement
defensive measures to handle common issues. If a user tries to withdraw more
than their current balance, the system should raise an "InsufficientFundsError".
Similarly, attempting to transfer a negative amount should trigger an
'InvalidAmountError'. These custom exceptions, along with others, will ensure that
errors are not only prevented but also communicated clearly to the user.
"""
# **********************************************************************************************************************
"""Start
    1. Ask user for email and PIN
    2. On successful login, create a pretend balance
    3. Offer options to:
        - Check balance
        - Transfer Funds
        - Make a Deposit
        - Withdraw Funds
    4. Check account limits and give confirmation prompts for each.
   End"""

import random as rd


class InsufficientFundsError(Exception):
    """Raised when there are not enough funds available"""
    pass

class InvalidSortCodeError(Exception):
    """Raised when Sort Code is in the wrong format"""
    pass

class InvalidAmountError(Exception):
    """Raised when a negative amount is entered"""
    pass

class InvalidAccountNumberError(Exception):
    """Raised when the Account Number is in the wrong format"""
    pass

def pin_check():
    # This function asks the user for a PIN and checks that it is in the correct format.
    while True:
        pin_code = input("Please enter your PIN : ")
        if len(pin_code) == 4 and pin_code.isdigit():
            break
        else:
            print("Invalid PIN, please try again.")
    return pin_code


def confirm_pin(pin):
    # This function checks that the user enters the same PIN as an existing one.
    # 3 attempts are allowed before the check is failed.
    for i in range(3):
        pin_code = pin_check()
        if pin_code != pin:
            print("Incorrect PIN")
            continue
        else:
            return True
    print("Too many incorrect PIN attempts made.")
    return False


print("Welcome to SafeBank, please log in to begin.")

# Asks for the user's email address and checks it is in the correct format:
while True:
    user_email = input("Please enter your email address : ")

    check_email = user_email.split("@")
    if len(check_email) == 2 and "." in check_email[1]:
        break
    else:
        print(f"{user_email} is not a valid email address format, please try again.")

# Asks for a PIN:
user_pin = pin_check()

# Allocates a random balance to the user following successful login:
user_balance = rd.randint(10, 99999)

#  Displays the menu for the user and prompts them to select an option:
print("Welcome! What would you like to do today?\nPlease choose from the following options:")

while True:
    print("""
    1. Check your balance
    2. Transfer Funds
    3. Make a deposit
    4. Withdraw Funds
    5. Log out
    """)

    user_choice = input("Please make your selection (enter the number) : ")

# ------------------------------------------------------------------------------------
    if user_choice == "5":  # Log out
        print("Thank you for using SafeBank.")
        break

# ------------------------------------------------------------------------------------
    elif user_choice == "1":  # Check balance
        print(f"Your current balance is £{user_balance:.2f}")

# ------------------------------------------------------------------------------------
    elif user_choice == "2":  # Transfer Funds
        try:
            print(f"You have £{user_balance:.2f} available.")
            transfer_amount = round(float(input("Please enter the amount you wish to transfer : ")), 2)

            # Checks the amount entered is valid, raises errors if it is negative or more than the balance:
            if transfer_amount > user_balance:
                raise InsufficientFundsError
            if transfer_amount < 0:
                raise InvalidAmountError

            # Asks for details of the target account, raises errors if input is in the wrong format:
            transfer_scode = input("Please enter the sort code of the account you wish to send money to: ")
            if len(transfer_scode) != 6 or not transfer_scode.isdigit():
                raise InvalidSortCodeError

            transfer_account = input("Please enter the account number you wish to send money to : ")
            if len(transfer_account) != 8 or not transfer_account.isdigit():
                raise InvalidAccountNumberError

            transfer_name = input("Please enter the name of the account you are sending money to : ")

            # Asks for the PIN to be reentered to confirm, then removes the transferred amount from the account:
            print(f"To confirm that you wish to transfer £{transfer_amount:.2f} to {transfer_name}")
            if confirm_pin(user_pin):
                user_balance -= transfer_amount
                print(f"Transaction successful. Your new balance is £{user_balance:.2f}")

        except InsufficientFundsError:
            print("Error: There are not enough funds available.")
        except InvalidAmountError:
            print("Error: The entered amount cannot be negative.")
        except InvalidSortCodeError:
            print("Error: Sort Codes must consist of 6 digits.")
        except InvalidAccountNumberError:
            print("Error: Account numbers must consist of 8 digits.")
        except ValueError:
            print("Error: Invalid input.")

# ------------------------------------------------------------------------------------
    elif user_choice == "3":  # Make a deposit
        # Repeatedly asks if the user wants to make deposits, until they are finished
        while True:
            print("""
Please choose from the following options:
    1. Deposit cheques
    2. Deposit cash
    3. Finish""")
            deposit_select = input("Please make your selection (1-3) : ")

            if deposit_select == "1":  # Deposit cheques
                # The user can enter several cheques, with a list keeping track of their values
                cheque_amounts = []
                while True:
                    try:
                        cheque_amount = round(float(input("Please enter the amount shown on the cheque : ")), 2)
                        if cheque_amount <= 0:
                            raise InvalidAmountError
                        cheque_amounts.append(cheque_amount)
                        # Asks the user if they would like to add more cheques:
                        add_another = input("Deposit another cheque? (y/n) : ").upper()
                        if add_another != "Y":
                            break
                    except ValueError:
                        print("Error: Invalid input.")
                    except InvalidAmountError:
                        print("Error: The entered amount must be greater than 0.")

                # Asks for the PIN to be confirmed before adding the cheques to the account:
                cheque_total = sum(cheque_amounts)
                print(f"To deposit {len(cheque_amounts)} cheques totalling £{cheque_total:.2f}")
                if confirm_pin(user_pin):
                    user_balance += cheque_total
                    print(f"Cheque deposit successful. Your new balance is £{user_balance:.2f}")

            elif deposit_select == "2":  # Deposit cash
                try:
                    cash_amount = round(float(input("Please enter the total amount of cash : ")), 2)
                    if cash_amount <= 0:
                        raise InvalidAmountError

                    # Asks for the PIN to be confirmed before adding the cash amount to the account:
                    print(f"To deposit £{cash_amount:.2f}")
                    if confirm_pin(user_pin):
                        user_balance += cash_amount
                        print(f"Cash deposit successful. Your new balance is £{user_balance:.2f}")

                except ValueError:
                    print("Error: Invalid input.")
                except InvalidAmountError:
                    print("Error: The entered amount must be greater than 0.")

            elif deposit_select == "3":  # Exit back to main menu
                break

            else:
                # This message is shown if the user enters something other than 1,2 or 3.
                print(f"{deposit_select} is not a valid selection, please choose from 1 to 3.")
# ------------------------------------------------------------------------------------
    elif user_choice == "4":  # Withdraw Funds
        try:
            print(f"You have £{user_balance:.2f} available.")
            withdraw_amount = round(float(input("Please enter the amount you wish to withdraw : ")), 2)

            # Checks the amount entered is valid, raises errors if it is negative or more than the balance:
            if withdraw_amount > user_balance:
                raise InsufficientFundsError
            if withdraw_amount < 0:
                raise InvalidAmountError

            # Asks for the PIN to be reentered to confirm, then removes the withdrawn amount from the account:
            print(f"To confirm that you wish to withdraw £{withdraw_amount:.2f}")
            if confirm_pin(user_pin):
                user_balance -= withdraw_amount
                print(f"Transaction successful. Your new balance is £{user_balance:.2f}")

        except InsufficientFundsError:
            print("Error: There are not enough funds available.")
        except InvalidAmountError:
            print("Error: The entered amount cannot be negative.")
        except ValueError:
            print("Error: Invalid input")
# ------------------------------------------------------------------------------------
    else:
        # This message is shown if the user has entered something other than 1,2,3,4 or 5.
        print(f"{user_choice} is not a valid selection, please choose from 1 to 5.")
