from socket import *
import sys

serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 12000
serverSocket.bind(('192.168.239.1',serverPort))
serverSocket.listen(1)

print('Server is ready to receive...')

while True:
    connectionSocket, addr = serverSocket.accept()
    print("Connection from IP:", addr[0],"\nSocket:",addr[1])

    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:],"rb")
        outputdata = f.read()

        if filename.endswith('.png'):
            content_type = 'image'
        elif filename.endswith('.ok'):
            content_type = 'ok'
        else:
            content_type = 'text'

        header = "HTTP/1.1 200 OK \nContent-Type: {}\r\n\r\n".format(content_type)
        connectionSocket.send(header.encode())
        print(header)

        connectionSocket.sendall(outputdata)
        connectionSocket.close()

    except IOError:
        error = "HTTP/1.1 404 Not Found \nContent-Type: text\r\n\r\n"
        error += "<html><head><title> 404NOTFOUND</title></head>"
        error += "<body style = 'text-align:center; background-color:#f1f1f1;>"
        error += "<h1 style>='color: #555555;'>Error 404 NOT FOUND </h1>"
        error += "<p style = 'font-size:18px;'> Sorry, request file could not be found.</p>"
        error += "</div></body></html>"
        connectionSocket.send(error.encode())
        connectionSocket.close()
        print("File not found")
    
serverSocket.close()
sys.exit()