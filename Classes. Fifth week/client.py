import socket
import time


class ClientError(Exception):
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        self.sock = socket.create_connection((host, port), timeout)
        
    def put(self, metric_name, value, timestamp=None):
        if timestamp is None:
            timestamp = int(time.time())
            
        self.sock.sendall(f'put {metric_name} {value} {timestamp}\n'.encode("utf8"))
        data = self.sock.recv(1024).decode("utf8")
        
        if data == 'error\nwrong command\n\n':
            raise ClientError 
            
    def get(self, metric_name):
        self.sock.sendall(f'get {metric_name}\n'.encode("utf8"))
        data = self.sock.recv(1024).decode("utf8")
        if data == 'ok\n\n':
            return {}
        
        if data[:2] != 'ok' or data[-2:] != '\n\n' or data == 'error\nwrong command\n\n':
            raise ClientError
            
        metrics_dict = {}
        try:
            for elem in data[3:-2].split('\n'):
                elem_list = elem.split(' ')
                if elem_list[0] in metrics_dict.keys():
                    metrics_dict[elem_list[0]].append((int(elem_list[2]), float(elem_list[1])))
                    metrics_dict[elem_list[0]].sort(key=lambda tup: tup[0])
                else:
                    metrics_dict[elem_list[0]] = [(int(elem_list[2]), float(elem_list[1]))]
            return metrics_dict
        except:
            raise ClientError

