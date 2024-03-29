import socket
import json
import os
import platform
import shutil
import time

def get_processes():
    """Получает информацию о всех процессах и сохраняет её в JSON файл."""
    processes = []
    os_type = platform.system()

    if os_type == 'Windows':
        command = 'tasklist'
    elif os_type in ['Linux', 'Darwin']:
        command = 'ps aux'

    for process in os.popen(command).readlines():
        processes.append(process.strip())

    return processes

def get_file_info(path):
    """Получает информацию о файлах и директориях в указанной директории."""
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
        print("Ждем подключения от клиентов...")
        client_socket, addr = server_socket.accept()
        print(f"Подключение установлено от {addr}")
        with client_socket:
            command = client_socket.recv(1024).decode()
            if command == "update_processes":
                process = get_processes()
                process_json = json.dumps(process)
                client_socket.sendall(process_json.encode('utf-8'))
            elif command == "set_directory":
                # Универсальный путь к директории
                new_directory = os.path.join(os.path.expanduser("~"), "PycharmProjects", "pythonProject", "PR2")
                os.makedirs(new_directory, exist_ok=True)
                os.chdir(new_directory)
                client_socket.sendall(b"Directory changed successfully.")
            elif command == "get_file_info":
                # Универсальный путь к директории
                downloads_directory = os.path.join(os.path.expanduser("~"), "Downloads")
                file_info = get_file_info(downloads_directory)
                json_data = json.dumps(file_info)
                client_socket.sendall(bytes(json_data, encoding="utf-8"))
            elif command == "move":
                # Универсальные пути к файлам
                source_file = os.path.join(os.path.expanduser("~"), "PycharmProjects", "pythonProject", "received_file.json")
                destination_directory = os.path.join(os.path.expanduser("~"), "PycharmProjects", "pythonProject", "PR2")
                shutil.move(source_file, destination_directory)
                client_socket.sendall(b"File moved successfully.")
            elif command == "exit":
                break
            else:
                client_socket.sendall(b"Invalid command.")

if __name__ == "__main__":
    main()