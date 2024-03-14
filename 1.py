import os
import json
from datetime import datetime
import socket

import os
import platform

def get_processes():
    """Получает информацию о всех процессах и сохраняет её в JSON файл."""
    processes = []
    os_type = platform.system() # Determine the OS type

    if os_type == 'Windows':
        # For Windows, use 'tasklist' command
        command = 'tasklist'
    elif os_type in ['Linux', 'Darwin']:
        # For Linux and macOS, use 'ps aux' command
        command = 'ps aux'
   
    for process in os.popen(command).readlines():
        processes.append(process.strip()) # удаляет пробелы в начале и конце строки strip()

    return processes



def server_loop(port):
    """Запускает сервер, который слушает на указанном порту."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # создает новый сокет. socket.AF_INET указывает, что сокет будет использовать IPv4 для сетевых адресов
        s.bind(('localhost', port)) #s.bind() привязывает сокет к определенному адресу и порту
        s.listen()
        print(f"Сервер запущен на порту {port}. Ожидание подключений...")
        while True:
            conn, addr = s.accept() #s.accept() блокирует выполнение кода, пока не будет установлено соединение с клиентом. Когда соединение установлено, s.accept() возвращает два значения: объект соединения (conn) и адрес клиента (addr).
            with conn:
                print(f"Подключение от {addr}")
                data = conn.recv(1024) # читает до 1024 байт данных из соединения
                command = data.decode()  #преобразует байты в текст
                if command == 'update_processes':
                    process = get_processes()
                    # Преобразование списка процессов в JSON
                    process_json = json.dumps(process)
                    conn.sendall(process_json.encode('utf-8')) ##Отправляет информауию обратно клиенту.  кодируется в байты с использованием UTF-8 перед отправкой.
                else:
                    conn.sendall('Неизвестная команда.'.encode('utf-8'))

                

if __name__ == '__main__':
    server_loop(48000)

#изменения в vetka2
    