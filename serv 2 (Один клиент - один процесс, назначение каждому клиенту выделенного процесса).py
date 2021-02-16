import multiprocessing
import os
import socket
import time


def run_server(port=53210):
    serv_sock = create_serv_sock(port)
    active_children = set()
    cid = 0
    while True:
        client_sock = accept_client_conn(serv_sock, cid)
        child_pid = serve_client(client_sock, cid)
        active_children.add(child_pid)
        #reap_children(active_children)
        cid += 1


def worker(client_sock, cid):
    request = read_request(client_sock)
    if request is None:
        print(f'Client #{cid} unexpectedly disconnected')
    else:
        response = handle_request(request)
        write_response(client_sock, response, cid)


def serve_client(client_sock, cid):
    p = multiprocessing.Process(target=worker(client_sock, cid))
    p.start()
    p.join()

    """
    child_pid = os.fork()
    if child_pid:
        # Родительский процесс, не делаем ничего
        client_sock.close()
        return child_pid

    # Дочерний процесс:
    #  - читаем запрос
    #  - обрабатываем
    #  - записываем ответ
    #  - закрываем сокет
    #  - завершаем процесс (os._exit())
    
    request = read_request(client_sock)
    if request is None:
        print(f'Client #{cid} unexpectedly disconnected')
    else:
        response = handle_request(request)
        write_response(client_sock, response, cid)
    os._exit(0)
    """

def reap_children(active_children):
    for child_pid in active_children.copy():
        child_pid, _ = os.waitpid(child_pid, os.WNOHANG)
        if child_pid:
            active_children.discard(child_pid)


def create_serv_sock(serv_port):
    serv_sock = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM,
                              proto=0)
    serv_sock.bind(('', serv_port))
    serv_sock.listen()
    return serv_sock


def accept_client_conn(serv_sock, cid):
    client_sock, client_addr = serv_sock.accept()
    print(f'Client #{cid} connected '
          f'{client_addr[0]}:{client_addr[1]}')
    return client_sock


def read_request(client_sock):
    request = bytearray()
    try:
        while True:
            chunk = client_sock.recv(1024)
            if not chunk:
                # Клиент преждевременно отключился.
                return None

            request += chunk
            return request

    except ConnectionResetError:
        # Соединение было неожиданно разорвано.
        return None
    except:
        raise


def handle_request(request):
    time.sleep(10)
    return request[::-1]


def write_response(client_sock, response, cid):
    client_sock.sendall(response)
    client_sock.close()
    print(f'Client #{cid} has been served')


if __name__ == '__main__':
    run_server()
