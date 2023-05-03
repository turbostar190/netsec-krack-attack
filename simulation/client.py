import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(("0.0.0.0", 2001))

class color:
    COLOR_CYAN = '\033[96m'
    COLOR_GREEN = '\033[92m'
    COLOR_RED = '\033[31m'
    COLOR_RESET = '\033[0m'

def send(message):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(message.encode(), ("127.0.0.1", 2002))
    s.close()
    print("Sending to ap: %s\n" % message)


def receive():
    global client_socket
    data, addr = client_socket.recvfrom(1024)
    message = data.decode("utf-8").replace("\0", "")
    print("Received: %s\n" % message)
    return message

def receive_noprint():
    global client_socket
    data, addr = client_socket.recvfrom(1024)
    message = data.decode("utf-8").replace("\0", "")
    return message

def wait():
    while True:
        msg = receive_noprint()
        if msg == "restart":
            break

if __name__ == "__main__":

    print("""
█▀ █░█ █▀█ █▀█ █░░ █ █▀▀ ▄▀█ █▄░█ ▀█▀
▄█ █▄█ █▀▀ █▀▀ █▄▄ █ █▄▄ █▀█ █░▀█ ░█░""")
          
    print()
    print("Waiting ANonce from AP...\n")
    message1 = receive()

    wait()

    print("Send Snonce to AP\n")
    send("message2(r, SNonce)")
    wait()

    print("Waiting GTK from AP...\n")
    message3 = receive()

    wait()

    print("[4/4] Sending message 4 to AP\n")
    send("message4(r+1)")
    print(color.COLOR_CYAN + "*** Installing PTK & GTK ***\n" + color.COLOR_RESET)

    wait()

    print("Sending data to AP\n")
    send("Enc(1,ptk){ Data(...) }")

    wait()

    message3_2 = receive()
    wait()

    # After reading msg3_2 the client answers with an encrypted message 4
    print("Sending message 4 to AP\n")
    send("Enc-2 ptk{ message4(r+2) }")
    print(color.COLOR_CYAN + "*** Reinstalling PTK & GTK ***\n" + color.COLOR_RESET)

    wait()

    wait()

    print(color.COLOR_RED + "*** Next transmitted frames will reuse nonces ***\n" + color.COLOR_RESET)

    print("Sending encrypted data to AP\n")
    send("Enc-1 ptk{ Data(...) }")
    

    print(color.COLOR_GREEN + "***END***\n" + color.COLOR_RESET)
    print(color.COLOR_GREEN + "Press Ctrl-D to exit\n" + color.COLOR_RESET)
    client_socket.close()
