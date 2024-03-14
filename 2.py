import socket
import json
from datetime import datetime
import os
import json

def send_command(command):
    """Отправляет команду на сервер и получает ответ."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #Создает новый сокет с использованием IPv4 (socket.AF_INET) и TCP (socket.SOCK_STREAM). 
        s.connect(('localhost', 48000))
        s.sendall(command.encode()) #Кодирует команду в байты и отправляет ее на сервер через сокет s. sendall гарантирует, что вся команда будет отправлена, даже если это потребует нескольких вызовов send.
        data = b'' # инициализирует переменную data пустым байтовым объектом. Этот объект будет использоваться для накопления полученных данных.
        while True:
            packet = s.recv(1024)
            if not packet: #проверяет, является ли полученный пакет пустым. Если это так, цикл прерывается, и функция переходит к декодированию данных.
                break
            data += packet
        try:
            # Декодирование JSON, если сервер отправляет данные в этом формате
            data_decoded = json.loads(data.decode())
        except json.JSONDecodeError:
            print("Ошибка декодирования JSON. Данные могут быть некорректными.")
            data_decoded = None
    return data_decoded

def save_received_file(data, file_format='json'):
    """Сохраняет полученные данные в файл."""
    timestamp = datetime.now().strftime('%d-%m-%Y/%H-%M-%S') 
    filename = os.path.join('.', timestamp.replace("/", "-") + f'.{file_format}')
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            if file_format == 'json':
                json.dump(data, f, indent=4)
            elif file_format == 'txt':
                f.write(data)
        print(f'Файл сохранен: {filename}')
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")

if __name__ == '__main__':
    command = 'update_processes'
    response = send_command(command)
    print(response)
    # Сохраняем путь к файлу, возвращенный сервером
    save_received_file(response, 'json')