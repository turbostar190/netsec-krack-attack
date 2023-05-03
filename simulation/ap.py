import socket

ap_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ap_socket.bind(("0.0.0.0", 2000))

class color:
    COLOR_CYAN = '\033[96m'
    COLOR_GREEN = '\033[92m'
    COLOR_RED = '\033[31m'
    COLOR_RESET = '\033[0m'

def send(message):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(message.encode(), ("127.0.0.1", 2002))
    s.close()
    print("Sending to client: %s\n" % message)


def receive():
    global ap_socket
    data, addr = ap_socket.recvfrom(1024)
    message = data.decode("utf-8").replace("\0", "")
    print("Received from client: %s\n" % message)
    return message


def receive_noprint():
    global ap_socket
    data, addr = ap_socket.recvfrom(1024)
    message = data.decode("utf-8").replace("\0", "")
    return message

def wait():
    while True:
        msg = receive_noprint()
        if msg == "restart":
            break

if __name__ == "__main__":
    print("""AUTHENTICATOR""")
    
    print()
    input(color.COLOR_GREEN + "Press <enter> to start the simulation...\n"+ color.COLOR_RESET)

    #send message 1/4
    print('[1/4] Sending the ANonce to client\n')
    send("message1(r, ANonce)")
    wait()

    #receive message 2/4
    print('[2/4] Waiting SNonce from client...\n')
    message2 = receive()
    wait()

    #send message 3/4
    print("[3/4] Sending GTK to client\n")
    send("messsage3(r+1; GTK)")

    wait()

    print('Waiting message 4 from client...\n')

    wait()

     # Receive msg 4
    print('Waiting message 4 from client...\n')
    
    wait()

    print('[3/4] Retransmitting message3 to ap\n')
    send("message3(r+2, GTK)")
    wait()

    
    message4_2 = receive()
    wait()


    message4_1 = receive()
    print('The AP accepts the older unencrypted message4\n')
    print(color.COLOR_CYAN + '*** Installs the PTK ***\n' + color.COLOR_RESET)
    wait()

    # Data exchange
    print("Waiting data from client...\n")
    data = receive()

    print(color.COLOR_GREEN + "***END***\n" + color.COLOR_RESET)
    print(color.COLOR_GREEN + "Press Ctrl-D to exit\n" + color.COLOR_RESET)
    ap_socket.close()