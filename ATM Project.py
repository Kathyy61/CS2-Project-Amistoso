accounts = { 
   233423:[1234, 50000, "Koki Monster", "20"],
   343565:[4545, 34500, "Elmo World", "20"],
   765345:[3456, 67990, "Kika Kim", "17"],
   234537:[5890, 34678, "Jacob Comp", "18"],
   987633:[4978, 89774, "Lashi Mash", "15"],
   563763:[2983, 56978, "Ken Neka", "13"],
   956893:[6789, 86437, "Pia Noe", "11"],
   103643:[7635, 62748, "Cab Bage", "13"],
   738453:[4579, 19467, "Ade Dase", "15"],
   573893:[4629, 29578, "Mol Lan", "24"],
   785633:[8649, 95682, "Kesha Mol","37"]   
}



def ATM():


    choice = -1


    while choice != 4:

        print("\nATM")
        print("1. Check accounts")
        print("2. Login to my account:D!")
        print("3. Register my new account:D")
        print("4. Exit")


        choice = int(input("Enter your choice: "))


        match choice:
            case 1:
                check_accounts(accounts)
            case 2:
                login()
            case 3:
                register_account(accounts)
            case 4:
                print("Exiting the app......")
            case _:
                print("Not in the choices na hahhaysttt2!!")



def check_accounts(accounts):
    for acc, details in accounts.items():
        print("Account:", acc, "Name:", details[2])



def register_account(accounts):
    account_number = int(input("Enter new account number: "))


    if account_number in accounts:

        print("Account already exists! Try another.")
        return


    pin = int(input("Enter new PIN: "))
    name = input("Enter your name: ")
    age = input("Enter your age: ")


    accounts[account_number] = [pin, 0, name, age]
    print("Account registered successfully yaeyy!!!")



def login():

    acc_num = int(input("Enter your account number: "))

    pin = int(input("Enter your pin: "))


    if acc_num in accounts and accounts[acc_num][0] == pin:

        print("Found! Logging in...")
    else:

        print("Wrong account number or pin uyyyy!!!")
        return


    choice = -1

    while choice != 7:

        print("1. Check Balance")
        print("2. Change Pin")
        print("3. Delete Account")
        print("4. Withdraw")
        print("5. Deposit")
        print("6. Pay Bills")
        print("7. Logout")


        choice = int(input("Enter your choice: "))


        match choice:

            case 1:
                print("Balance:", accounts[acc_num][1])
            case 2:
                change_pin(acc_num)
            case 3:
                delete_account(acc_num)
                break
            case 4:
                withdraw(acc_num)
            case 5:
                deposit(acc_num)
            case 6:
                bills(acc_num)
            case 7:
                print("Logging out...")
            case _:
                print("Not in the choices...")

def change_pin(acc):

    old_pin = int(input("Enter old pin: "))
    new_pin = input("Enter new pin: ")
    confirm_pin = input("Confirm new pin: ")

    if old_pin == accounts[acc][0] and new_pin == confirm_pin:
        if len(new_pin) == 4 and new_pin.isdigit():

            accounts[acc][0] = int(new_pin)

            print("Pin changed successfully yayy!!")
        else:
            print("PIN must be 4 digits")
    else:
        print("Wrong pin uyyyy!!")

def delete_account(acc):

    option = input("Are you sure you want to delete your account????? y/n: ")

    if option.lower() == "y":
        accounts.pop(acc)
        print("Account deleted successfully!!!")
    else:
        print("Account delete cancelled")


def withdraw(acc):
    amount = int(input("Enter amount to withdraw: "))
    if amount > 0 and amount <= accounts[acc][1]:
        accounts[acc][1] -= amount
        print("Withdrew successfully wowww!!!")
    else:
        print("Cannot withdraw that amount uyyy!!")

def deposit(acc):
    amount = int(input("Enter amount to deposit: "))
    if amount > 0:
        accounts[acc][1] += amount
        print("Deposit successful wowww!!")
    else:
        print("Cannot deposit that amount of money uyyy!!!")


def bills(acc):

    choice = -1


    while choice != 5:

        print("Pay Bills")
        print("1. PLDT")
        print("2. Water")
        print("3. Shoppee")
        print("4. ZANECO")
        print("5. Back")

        choice = int(input("Enter your choice: "))


        match choice:
            case 1:
                amount = int(input("Enter PLDT bill amount: "))
                
           
            case 2:
                amount = int(input("Enter Water bill amount: "))

            case 3:
                amount = int(input("Enter Shoppe bill amount: "))

            case 4:
                amount = int(input("Enter ZANECO bill amount: "))
            case 5:
                break
            case _:
                print("Not in the choices uyyy!!")
                continue
        if choice in [1,2,3,4]:
                if amount > 0 and amount <= accounts[acc][1]:
                 accounts[acc][1] -= amount
                 print("Bill paid successfully yayy!!!")
                else:
                 print("Not enough money huyy")


ATM()