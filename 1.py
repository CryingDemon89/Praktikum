# программа1
import shutil
import socket
import json
import os
import time


def get_file_info(path):
    file_info = {}
    for root, dirs, files in os.walk(path):
        file_info[root] = {
            "dirs": dirs,
            "files": files
        }
    return file_info


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12347))
    server_socket.listen()
    while True:
        print("Ждем подключения от программы 2...")
        client_socket, addr = server_socket.accept()
        print("Подключение установлено!")
        with client_socket:
            command = client_socket.recv(1024).decode()
            if command == "set_directory":
                new_directory = "C:\\Users\\Nata\\PycharmProjects\\pythonProject\\PR2"
                os.makedirs(new_directory)
                if os.path.isdir(new_directory):
                    os.chdir(new_directory)
                    client_socket.sendall(b"Directory changed successfully.")
                else:
                    time.sleep(3)
                    if os.path.isdir(new_directory):
                        os.chdir(new_directory)
                        client_socket.sendall(b"Directory changed successfully.")
                    else:
                        client_socket.sendall(b"Invalid directory.")

            elif command == "get_file_info":
                file_info = get_file_info("../../Downloads")
                json_data = json.dumps(file_info)
                client_socket.sendall(bytes(json_data, encoding="utf-8"))
                print('!', json_data)

            elif command == "move":
                def move_file(source_file, destination_directory):
                    shutil.move(source_file, destination_directory)

                source_file = "C:\\Users\\Nata\\PycharmProjects\\pythonProject\\received_file.json"
                destination_directory = "C:\\Users\\Nata\\PycharmProjects\\pythonProject\\PR2"

                move_file(source_file, destination_directory)

            elif command == "exit":
                break

            else:
                client_socket.sendall(b"Invalid command.")


if __name__ == "__main__":
    main()
