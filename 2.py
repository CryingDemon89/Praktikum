import socket
import json


def main():
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 12347))
            print()
            command = input("Enter a command: set_directory, get_file_info, move, exit")
            if command == "exit":
                s.sendall(command.encode())
                break  # выход из цикла и завершение программы
            else:
                s.sendall(command.encode())
                data = b''
                while True:
                    packet = s.recv(1024)
                    if not packet:
                        break
                    data += packet
                try:
                    data_decoded = json.loads(data.decode())
                    print(data_decoded)
                    with open("received_file.json", 'w') as file:
                        file.write(data.decode())
                        print("File successfully received!")
                except json.JSONDecodeError:
                    if data.decode() == "Directory changed successfully.":
                        print("Directory changed successfully.")
                    else:
                        print("Error: " + data.decode())


if __name__ == "__main__":
    main()
