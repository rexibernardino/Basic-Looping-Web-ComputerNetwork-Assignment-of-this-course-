import socket #import socket module
serverName = '' 
serverPort = 10000 


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating socket obejct
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #set the socket option SO_REUSEADDR to get the same address after closing
serverSocket.bind((serverName, serverPort)) # bind the socket based on name and port number
serverSocket.listen(1) # set the socket to a maximum of 1 connection established
print('Server is running ... \n Connected port %s ...' % serverPort) #display message to let the user know the server is running

while True:    
 
    clientConnection, clientAddress = serverSocket.accept() #accept connection from client

    clientRequest = clientConnection.recv(1024).decode() #receive data from server
    print(clientRequest) #display the data that has been received
    
    headers = clientRequest.split('\n') #separates the HTTP request headers sent by the client into separate header lines in a list.
    path = headers[0].split()[1] #get path from request HTTP
    htmlFile = "" #declare htmlFile
   
    if path == '/':
        htmlFile = 'index.html' #set htmlFile into a html file index.html
    
    try:
        fileOpen = open(htmlFile) #open htmlFile based on condition
        result = fileOpen.read() #save variable to result
        fileOpen.close() #close opened htmlFile

        response = 'HTTP/1.0 200 OK\n\n' + result #the response that is displayed to the web client when the web result is executed according to the conditions typed by the client
    except FileNotFoundError:

        response = 'HTTP/1.0 404 NOT FOUND\n\n404 NOT FOUND' #error response when the condition is not met
    clientConnection.sendall(response.encode()) #send data to server and encode it beforehand
    clientConnection.close() #close or stop connection

