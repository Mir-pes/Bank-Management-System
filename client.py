import socket

class BankClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
        self.client_socket.connect(("10.1.19.197", 5555))

    def send_request(self, request):
        try:
            self.client_socket.send(request.encode("utf-8"))
            response = self.client_socket.recv(1024).decode("utf-8")
            print(response)
        except Exception as e:
            print(f"Error: {e}")

    def login(self, account_name, password):
        self.send_request(f"LOGIN {account_name} {password}")

    def open_account(self, account_name, password):
        self.send_request(f"OPEN {account_name} {password}")

    def deposit(self, account_name, password, amount):
        self.send_request(f"DEPOSIT {account_name} {password} {amount}")

    def withdraw(self, account_name, password, amount):
        self.send_request(f"WITHDRAW {account_name} {password} {amount}")

    def check_balance(self, account_name, password):
        self.send_request(f"BALANCE {account_name} {password}")

    def start_menu(self):
        while True:
            print("1. Open Account")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Check Balance")
            print("5. Exit")

            choice = input("Enter your choice (1-5): ")

            if choice == "1":
                account_name = input("Enter account name: ")
                password = input("Enter password: ")
                self.open_account(account_name, password)

            elif choice == "2":
                account_name = input("Enter account name: ")
                password = input("Enter password: ")
                amount = input("Enter amount to deposit: ")
                self.deposit(account_name, password, amount)

            elif choice == "3":
                account_name = input("Enter account name: ")
                password = input("Enter password: ")
                amount = input("Enter amount to withdraw: ")
                self.withdraw(account_name, password, amount)

            elif choice == "4":
                account_name = input("Enter account name: ")
                password = input("Enter password: ")
                self.check_balance(account_name, password)

            elif choice == "5":
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    try:
        bank_client = BankClient()
        bank_client.start_menu()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        bank_client.client_socket.close()