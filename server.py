import socket
import json

address = "localhost"
port = 3000
data_package_size = 1024
score = [20, 20]


def start_server():
    print(f"Сервер c адресом [{address}] и портом [{port}] успешно запущен")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((address, port))
        server.listen(2)
        first_user, address_of_first_user = server.accept()
        print(f'{address_of_first_user} успешно подключился')
        coordinates_of_first_user = first_user.recv(data_package_size).decode('utf-8')
        coordinates_of_first_user = json.loads(coordinates_of_first_user)
        print(coordinates_of_first_user)
        second_user, address_of_second_user = server.accept()
        print(f'{address_of_second_user} успешно подключился')
        coordinates_of_second_user = second_user.recv(data_package_size).decode('utf-8')
        coordinates_of_second_user = json.loads(coordinates_of_second_user)
        print(coordinates_of_second_user)
        start_battle(first_user, coordinates_of_first_user, second_user, coordinates_of_second_user)


def start_battle(first_user, coordinates_of_first_user, second_user, coordinates_of_second_user):
    first_user.sendall('1'.encode('utf-8'))
    second_user.sendall('2'.encode('utf-8'))
    while True:
        data = first_user.recv(1024).decode('utf-8')
        second_user.sendall(data.encode('utf-8'))
        message = check_salvo(coordinates_of_second_user, data, 1)
        first_user.sendall(message.encode('utf-8'))
        check_victory(first_user, second_user)
        while message == 'hit' or message == 'destroyed':
            data = first_user.recv(1024).decode('utf-8')
            second_user.sendall(data.encode('utf-8'))
            message = check_salvo(coordinates_of_second_user, data, 1)
            first_user.sendall(message.encode('utf-8'))
            check_victory(first_user, second_user)
        data = second_user.recv(1024).decode('utf-8')
        first_user.sendall(data.encode('utf-8'))
        message = check_salvo(coordinates_of_first_user, data, 0)
        second_user.sendall(message.encode('utf-8'))
        check_victory(first_user, second_user)
        while message == 'hit' or message == 'destroyed':
            data = second_user.recv(1024).decode('utf-8')
            first_user.sendall(data.encode('utf-8'))
            message = check_salvo(coordinates_of_first_user, data, 0)
            second_user.sendall(message.encode('utf-8'))
            check_victory(first_user, second_user)


def check_victory(player1, player2):
    if score[0] <= 0:
        player2.sendall('win'.encode('utf-8'))
        player1.sendall('lose'.encode('utf-8'))
    elif score[1] <= 0:
        player1.sendall('win'.encode('utf-8'))
        player2.sendall('lose'.encode('utf-8'))


def check_salvo(coordinates_of_user, data, enemy_index):
    for i in range(len(coordinates_of_user)):
        for j in range(len(coordinates_of_user[i])):
            if [int(data[0]), int(data[1])] == coordinates_of_user[i][j]:
                score[enemy_index] -= 1
                coordinates_of_user[i][j] = [-1, -1]
                for k in range(len(coordinates_of_user[i])):
                    if coordinates_of_user[i][k] != [-1, -1]:
                        return str("hit")
                return str("destroyed")
    return str("miss")


if __name__ == "__main__":
    start_server()
