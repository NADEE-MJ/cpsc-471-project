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
    welcomeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    welcomeSocket.bind(("", serverPort))

    return welcomeSocket


def receive_command(controlSocket):
    command_length = int(
        receive_bytes_from_socket(controlSocket, BYTES_PER_PACKET)
        .decode("utf-8")
        .strip("0")
    )
    command = receive_bytes_from_socket(controlSocket, command_length).decode("utf-8")
    return command


def receive_bytes_from_socket(socket, num_bytes):
    """
    Receives the specified number of bytes from the specified socket

    Parameters:
        socket (socket): the socket from which to receive
        num_bytes (int): the number of bytes to receive

    Returns:
        bytes: the bytes received
    """
    main_buffer = b""

    temp_buffer = b""

    # Keep receiving till num_bytes bytes is received
    while len(main_buffer) < num_bytes:
        # Attempt to receive bytes
        temp_buffer = socket.recv(num_bytes)

        # The other side has closed the socket
        if not temp_buffer:
            break

        main_buffer += temp_buffer

    return main_buffer


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

    print("Waiting for connections...")

    clientSock, addr = welcomeSock.accept()
    print("Accepted connection from client: ", addr)
    print("\n")

    while True:
        command = receive_command(clientSock)

        check_command(command, clientSock)

        if command == "ls":
            print("received ls")
    clientSock.close()


if __name__ == "__main__":
    main()
