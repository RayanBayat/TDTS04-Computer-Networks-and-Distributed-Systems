import socket
import sys



if len(sys.argv)<3 or len(sys.argv) > 3: #give error if argument is not compatiple and exit
    print("You need to give Ip and port. example =  python server.py 127.192.3.2 9999")
    sys.exit(1)


class Server:
    def __init__(self,ipaddress, portnumber): #server class contructor
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a tcp socket
        self.serverSocket.bind((ipaddress,portnumber)) #bind it to given ip and port number
        self.serverSocket.listen(1) # amount of devices to listen to


first = Server(sys.argv[1],int(sys.argv[2])) #create an object of our server
   
#first = Server("127.192.3.2",9999)     
print('server socket created')
print('listening to port: ' + sys.argv[2])
city = 'Linköping'
cityb = bytes(city, encoding = 'utf-8')
while 1:
    while 1:
        try:
           conn,client_address = first.serverSocket.accept() #handshake socket
           break
        except : 
            print('error')
            pass

    request = conn.recv(4096) #get requests from client
    first_line = request.split(b'\n')[0] #string manipulation to get url
    request = request.replace(b"Connection: keep-alive",b"Connection: close") #change connection type to closed
  
    try:
        url = first_line.split(b' ')[1]
    except :
        
        pass
  

    http_pos = url.find(b"://") # find pos of ://
    

    if (http_pos==-1):
       
        temp = url
    else:
        temp = url[(http_pos+3):] # get the rest of url
   
    if (temp.find(b"smiley") != -1):
        temp = temp.replace(b"smiley",b"trolly")
        request = request.replace(b"smiley",b"trolly")
        pass
 
   
    

    port_pos = temp.find(b":") 

    

    webserver_pos = temp.find(b"/")
    if webserver_pos == -1:
        webserver_pos = len(temp)
  

    webserver = ""
  
    port = 80 
    webserver = temp[:webserver_pos] 

   
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.connect((webserver, port))
    s.sendall(request)

    while 1:
        
       
        try:
            data = s.recv(4096)
        except:
            pass
       
        if (data.find(b"Content-Type: text") != -1 ):
            data = data.replace(b'Smiley', b'Trolly')
            
            data = data.replace(b'Stockholm',cityb)
            if (data.find(b"/" + cityb) != -1):

                data = data.replace(b"/"+cityb,b'/Stockholm')
                pass
       
        #print(data)
        if (data != b''):

            conn.sendall(data) # send to browser/client
        else:
         
            break
