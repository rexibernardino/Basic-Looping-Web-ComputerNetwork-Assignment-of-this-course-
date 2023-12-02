import socket #import socket module
import sys #import sys module to terminate the program
serverName = '192.168.239.1' 
serverPort = 16000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating socket object

#Prepare a server socket
serverSocket.bind((serverName,serverPort)) #bind socket based on name and port number
serverSocket.listen(1)#set maximum connection established of 1
print('Server is running ... \nConnected port %s ...' % serverPort) #display message to let the user know the server is running

while True:
    #Establish the connection
    connectionSocket, addr = serverSocket.accept() #accept connection from client
    print("Connection IP: ", addr[0],"\nSocket: ",addr[1]) #display IP and socket info of client
    try:
        message = connectionSocket.recv(1024).decode()#receive data and decode from client
        m = message.split()#use to check if message is empty or not
        if m: #check if message is empty or not
            filename = message.split()[1]#get the filename from request
            print(message,'\n')#print detailed message 
            headers = message.split('\n')#get the headers sent by client
            path = headers[0].split()[1] #get path from request HTTP
            print(path,'\n') #print the path
            f = open(filename[1:])#open the filename
            outputdata = f.read()#read the filename and save it to variable
            #Send one HTTP header line into socket
            header = 'HTTP/1.1 200 OK\r\n\r\n'
            connectionSocket.send(header.encode())#send the response header to client
            print(header)#print the header
            #Send the content of the requested file to the client
            connectionSocket.sendall(outputdata.encode())#send the data file to client
            connectionSocket.send("\r\n".encode())#send next line
            connectionSocket.close()#close the connection
        else:
            connectionSocket.close()#close the connection
    except IOError or IndexError or FileNotFoundError:
        error ='HTTP/1.1 404 NOT FOUND\r\n\r\n'
        error += "<html><head><title>TEXT HTML</title><style>"
        error += "body {display: flex;align-items: center;justify-content: center;height: 100vh;margin: 0;}"
        error +=".form-container {text-align: center;}</style></head>"
        error += '<body><div class="form-container"><!-- <h1>TEXT HTML</h1> --><h1>404 | Not Found</h1></form><br></div></body></html>'
        connectionSocket.send(error.encode())
        connectionSocket.close()
        print("404 Not Found")

#Close the server socket      
serverSocket.close()
sys.exit()