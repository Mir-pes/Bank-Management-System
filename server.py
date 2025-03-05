import socket
import threading

class BankServer:
    def __init__(self):
        self.accounts = {}

    def handle_client(self, client_socket, addr):
        print(f"Accepted connection from {addr}")

        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break

                decoded_data = data.decode("utf-8")
                command, *params = decoded_data.split()

                if command == "OPEN" and len(params) == 2:
                    account_name, password = params
                    if account_name not in self.accounts:
                        self.accounts[account_name] = {'balance': 0, 'password': password}
                        response = "Account opened successfully!"
                    else:
                        response = "Account with that name already exists. Please choose a different name."

                elif command in ["DEPOSIT", "WITHDRAW"] and len(params) == 3:
                    account_name, password, amount = params
                    if self.authenticate(account_name, password):
                        if command == "DEPOSIT":
                            self.accounts[account_name]['balance'] += float(amount)
                            response = f"Deposited {amount} into account {account_name}"
                        elif command == "WITHDRAW":
                            if self.accounts[account_name]['balance'] >= float(amount):
                                self.accounts[account_name]['balance'] -= float(amount)
                                response = f"Withdrew {amount} from account {account_name}"
                            else:
                                response = "Insufficient funds"
                    else:
                        response = "Authentication failed. Incorrect password."

                elif command == "BALANCE" and len(params) == 2:
                    account_name, password = params
                    if self.authenticate(account_name, password):
                        response = f"Balance for account {account_name}: {self.accounts[account_name]['balance']}"
                    else:
                        response = "Authentication failed. Incorrect password."

                else:
                    response = "Invalid command or incorrect parameters"

                client_socket.send(response.encode("utf-8"))

        except Exception as e:
            print(f"Error: {e}")

        print(f"Connection from {addr} closed")
        client_socket.close()

    def authenticate(self, account_name, password):
        return account_name in self.accounts and self.accounts[account_name]['password'] == password

    def start(self, host, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        n = int(input("Enter the maximum number of simultaneous clients: "))
        server_socket.listen(n)
        print(f"Server listening on {host}:{port} with a maximum of {n} simultaneous clients")

        try:
            while True:
                client_socket, addr = server_socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                client_thread.start()

        except KeyboardInterrupt:
            print("Server shutting down.")
            server_socket.close()

if __name__ == "__main__":
    bank_server = BankServer()
    bank_server.start("10.1.19.197", 5555)
