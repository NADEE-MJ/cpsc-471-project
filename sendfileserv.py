import socket
import sys


BYTES_PER_PACKET = 10


def print_file_help():
    print(
        (
            f"USAGE python {sys.argv[0]} <PORT>\n"
            f"\t<PORT>: The port number to host the server on, defaults to 1234\n\n"
            f"\t-h, --help: show this help message and exit\n"
        )
    )


def print_command_help():
    print(
        (
            f"USAGE <command> <parameters?>\n"
            f"  command options:\n"
            f"\tget <filename>: download a file from the folder where the server is running from\n"
            f"\tput <filename>: upload a file from the folder where the cli is located to the server\n"
            f"\tls: show all files on the server\n"
            f"\tquit: exit the program\n"
            f"\thelp: show this help message and exit\n"
        )
    )


def check_file_args():
    if len(sys.argv) >= 2 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
        print_file_help()
        sys.exit(0)
    elif len(sys.argv) > 2:
        print("Too many arguments.")
        print_file_help()
        sys.exit(1)

    # Server port
    serverPort = int(sys.argv[1]) if len(sys.argv) >= 2 else 1234

    return serverPort


def create_control_socket_server(serverPort):
    # Create a welcome socket.
    welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    welcomeSock.bind(("", serverPort))

    return welcomeSock


def receive_command(controlSocket):
    # The buffer
    recvBuff = b""

    # The temporary buffer
    tmpBuff = b""

    # Keep receiving till all is received
    while len(recvBuff) < BYTES_PER_PACKET:
        # Attempt to receive bytes
        tmpBuff = controlSocket.recv(BYTES_PER_PACKET)
        print(tmpBuff)

        # The other side has closed the socket
        if not tmpBuff:
            break

        # Add the received bytes to the buffer
        recvBuff += tmpBuff

    command_string = recvBuff.decode("utf-8")

    return command_string


# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
def receive_all(socket, num_bytes):
    # The buffer
    receive_buffer = b""

    # The temporary buffer
    tmpBuff = b""

    # Keep receiving till all is received
    while len(recvBuff) < numBytes:
        # Attempt to receive bytes
        tmpBuff = sock.recv(numBytes)
        print(tmpBuff)

        # The other side has closed the socket
        if not tmpBuff:
            break

        # Add the received bytes to the buffer
        recvBuff += tmpBuff

    return recvBuff


def get_file(controlSocket, serverAddress, fileName):
    # The buffer to all data received from the
    # the client.
    fileData = ""

    # The temporary buffer to store the received
    # data.
    recvBuff = ""

    # The size of the incoming file
    fileSize = 0

    # The buffer containing the file size
    fileSizeBuff = ""

    # Receive the first 10 bytes indicating the
    # size of the file
    fileSizeBuff = recvAll(clientSock, 10)

    # Get the file size
    fileSize = int(fileSizeBuff)

    print("The file size is ", fileSize)

    # Get the file data
    fileData = recvAll(clientSock, fileSize)

    print(fileData.decode("utf-8"))

    print("The file data is: ")
    print(fileData)

    # Close our side
    clientSock.close()


def main():
    serverPort = check_file_args()

    # Create a welcome socket.
    welcomeSock = create_control_socket_server(serverPort)

    # Start listening on the socket
    welcomeSock.listen(1)

    while True:
        print("Waiting for connections...")

        # Accept connections in a with statement
        clientSock, addr = welcomeSock.accept()

        receive_command(clientSock)
        receive_command(clientSock)

        print("Accepted connection from client: ", addr)
        print("\n")

        clientSock.close()


if __name__ == "__main__":
    main()
