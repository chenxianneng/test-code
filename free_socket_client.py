import socket
import time
import threading

stop = False
connect_count = 0

lock = threading.Lock()

def run():
    HOST = '192.168.1.104'  # The server's hostname or IP address
    PORT = 9734        # The port used by the server
    global stop
    global connect_count

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            lock.acquire()
            connect_count += 1
            lock.release()
            while True:
                s.sendall(b'A')
                data = s.recv(1024)
                #print('Received', repr(data))
                time.sleep(1)        
    except Exception as e:
        #print(e)
        pass

while True:
    thread1 = threading.Thread(target=run)
    thread1.start()
    #connect_count += 1
    print(connect_count)
    #time.sleep(1)

input('input: \n')
#thread1.join()

