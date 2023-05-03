import socket

mitm_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mitm_socket.bind(("0.0.0.0", 2002))

class color:
    COLOR_CYAN = '\033[96m'
    COLOR_GREEN = '\033[92m'
    COLOR_RED = '\033[31m'
    COLOR_RESET = '\033[0m'

def to_client(message):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(message, ("127.0.0.1", 2001))
    s.close()
    message  = message.decode("utf-8").replace("\0","")
    if message != "restart":
        print("Sending: %s to client\n" % message)

def to_ap(message):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(message, ("127.0.0.1", 2000))
    s.close()
    message = message.decode("utf-8").replace("\0", "") 
    if message != "restart":
        print("Send: %s to AP\n" % message)

def to_all(message):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(message, ("127.0.0.1", 2001))
    s.sendto(message, ("127.0.0.1", 2000))
    s.close()

def receive():
    global mitm_socket
    data, addr = mitm_socket.recvfrom(1024)
    message = data.decode("utf-8").replace("\0", "")
    print("Received : %s\n" % message)
    return data

def contin():
    flag = input(color.COLOR_GREEN + "Press <enter> to continue\n" + color.COLOR_RESET)
    
if __name__ == "__main__":
    print("""
█▀▄▀█ █ ▀█▀ █▀▄▀█
█░▀░█ █ ░█░ █░▀░█""")
    
    print()
    
    # MitM intercepts and sends message1
    message1 = receive()
    contin()
    to_client(message1)
    to_all("restart".encode())

    # MitM intercepts and sends message2
    message2 = receive()
    contin()
    to_ap(message2)
    to_all("restart".encode())

    # MitM intercepts and sends message3 
    message3 = receive()
    contin()
    to_client(message3)
    to_all("restart".encode())      #modficato

    # MitM intercepts and blocks message4 coming from client
    print(color.COLOR_RED + "MitM Intercepts and blocks message4 of the handshake\n" + color.COLOR_RESET)
    message4 = receive()
    contin()
    to_all("restart".encode())

    #Mitm intercepts and sends the retransmission of message3
    print(color.COLOR_RED + "MitM intercepts and blocks the transmission of data\n" + color.COLOR_RESET)
    message3_2 = receive()
    contin()
    to_all("restart".encode())

    print(color.COLOR_RED + "MITM forwards the message3 to client\n" + color.COLOR_RESET)
    message3_3 = receive()
    contin()
    to_client(message3_3)
    to_all("restart".encode()) 

    #Mitm intercepts and sends the encrypted message4
    print(color.COLOR_RED + "MitM intercepts and forwards the encrypted message4\n" + color.COLOR_RESET)
    message4_2 = receive()
    contin()
    to_ap(message4_2)
    to_all("restart".encode())

    
    print(color.COLOR_RED + "MitM sends to AP the old message4 of the handshake\n" + color.COLOR_RESET)
    to_ap("message4(r+1)".encode())
    to_all("restart".encode())

    # MitM intercepts and sends message2
    data = receive()
    contin()
    to_ap(data)
    to_all("restart".encode())

    print(color.COLOR_GREEN + "***END***\n" + color.COLOR_RESET)
    print(color.COLOR_GREEN + "Press Ctrl-D to exit\n" + color.COLOR_RESET)
    mitm_socket.close()
