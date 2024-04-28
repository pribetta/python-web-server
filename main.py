# Uncomment this to pass the first stage
import socket
from threading import Thread
import sys
import os

def http_server_task(conn,add):
    with conn:
        data = conn.recv(1024)
        if not data:
            return
        #print(f"Received {data}")
        str = data.decode('utf-8')
        print(str)
        path = str.split("\r\n")[0].split(" ")[1]
        if(path.startswith("/echo/")):
            path = path[6:]
            resp_str = f"HTTP/1.1 200 OK \r\nContent-Type: text/plain \r\nContent-Length: {len(path)}\r\n\n{path}\r\n\r\n"
        elif path=="/":
            resp_str = f"HTTP/1.1 200 OK \r\n\r\n"
        elif path.startswith("/user-agent"):
            ua = str.split("\r\n")[2].split(" ")[1]
            resp_str = f"HTTP/1.1 200 OK \r\nContent-Type: text/plain \r\nContent-Length: {len(ua)}\r\n\n{ua}\r\n\r\n"
        elif str.split("\r\n")[0].split(" ")[0]=="POST" and path.startswith("/files"):
            dir = sys.argv[2]
            filename = path[7:]
            body = str.split("\r\n")[-1]
            print(f"body is {body}")
            filepath=f"{dir}{filename}"
            with open(filepath, "w") as f: f.write(f"{body}")
            resp_str = "HTTP/1.1 201 CREATED\r\n\r\n"
        elif path.startswith("/files/"):
            filename = path[7:]
            print(sys.argv)
            foldername = sys.argv[2]
            print(foldername)
            p = f"{foldername}{filename}"
            print(p)
            if(os.path.exists(p)) :
                with open(p) as f: s = f.read()
                resp_str = f"HTTP/1.1 200 OK \r\nContent-Type: application/octet-stream \r\nContent-Length: {len(s)}\r\n\n{s}\r\n\r\n"
            else:
                resp_str = "HTTP/1.1 404 NOT FOUND \r\n\r\n"

        else:
            resp_str = "HTTP/1.1 404 NOT FOUND \r\n\r\n"
        #print(f"Path is {path}")
        
        print(f"{resp_str}")
        resp = resp_str.encode('utf-8')
        #if(path == "/"):
        conn.sendall(resp)

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    count=0
    threads=[]
    while True:
        conn, add = server_socket.accept() # wait for client
        threads.append(Thread(group=None, 
                                target = http_server_task,
                                name=f"Thread{count}",
                                args = (conn,add),
                                daemon=None
                               ))
        threads[count].start()
        count=count+1

    for i in count:
        threads[i].join()
    
    

    

    
    #else:
    #    conn.sendall("HTTP/1.1 404 NOT FOUND\r\n\r\n".encode("utf-8"))
    #conn.sendall("HTTP/1.1 200 OK\r\n\r\n".encode("utf-8"))
    #conn.close()


if __name__ == "__main__":
    main()
