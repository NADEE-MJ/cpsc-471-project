import socket
import os
import sys


def print_file_help():
    print(
        (
            f"USAGE python {sys.argv[0]} <SERVER IP> <SERVER PORT>\n"
            f"\t<SERVER IP>: IP address of the server, defaults to localhost\n"
            f"\t<SERVER PORT>: Port number of the server, defaults to 1234\n\n"
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
    elif len(sys.argv) > 3:
        print("Too many arguments.")
        print_file_help()
        sys.exit(1)

    # Server Address / IP
    serverAddress = sys.argv[1] if len(sys.argv) > 1 else "localhost"

    # Server port
    serverPort = int(sys.argv[2]) if len(sys.argv) > 2 else 1234

    return serverAddress, serverPort


def connect_to_server(serverAddress, serverPort):
    # Create a TCP socket
    connectionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    connectionSocket.connect((serverAddress, serverPort))

    return connectionSocket


def create_ephemeral_socket_server():
    # Create a welcome socket.
    welcomeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to port 0
    welcomeSocket.bind(("", 0))

    # Retreive the ephemeral port number
    ephemeralPort = welcomeSocket.getsockname()[1]

    # get socket ip
    address = socket.gethostbyname(socket.gethostname())

    return welcomeSocket, ephemeralPort, address


#! might just be able to make this a send_data function to be reused elsewhere
def send_command(controlSocket, command):
    dataSizeStr = str(len(command))

    # Prepend 0's to the size string
    # until the size is 10 bytes
    while len(dataSizeStr) < 10:
        dataSizeStr = "0" + dataSizeStr

    # Prepend the size of the data to the
    # file data.
    data = dataSizeStr + command

    # The number of bytes sent
    numSent = 0

    # Send the data!
    while len(data) > numSent:
        numSent += controlSocket.send(data[numSent:].encode("utf-8"))


def get_file(controlSocket, serverAddress, fileName):
    print("Receiving file...")
    #! WRITE CODE FOR RECEIVING FILE
    # controlSocket.send(command.encode("utf-8"))
    # controlSocket.send(fileName.encode("utf-8"))
    # fileObj = open(fileName, "w")
    # while True:
    #     data = controlSocket.recv(1024).decode("utf-8")
    #     if not data:
    #         break
    #     fileObj.write(data)
    # fileObj.close()


def put_file(controlSocket, serverAddress, fileName):
    if not os.path.isfile(fileName):
        print("File does not exist")

    #! WRITE CODE FOR SENDING FILE
    # controlSocket.send(command.encode("utf-8"))
    # controlSocket.send(fileName.encode("utf-8"))
    # print("Sending file...")
    # put_file(controlSocket, fileName)
    # print("File sent")
    # # Open the file
    # fileObj = open(fileName, "r")

    # # The number of bytes sent
    # numSent = 0

    # # The file data
    # fileData = None

    # # Keep sending until all is sent
    # while True:
    #     # Read 65536 bytes of data
    #     fileData = fileObj.read(65536)

    #     # Make sure we did not hit EOF
    #     if fileData:
    #         # Get the size of the data read
    #         # and convert it to string
    #         dataSizeStr = str(len(fileData))

    #         # Prepend 0's to the size string
    #         # until the size is 10 bytes
    #         while len(dataSizeStr) < 10:
    #             dataSizeStr = "0" + dataSizeStr

    #         # Prepend the size of the data to the
    #         # file data.
    #         fileData = dataSizeStr + fileData

    #         # The number of bytes sent
    #         numSent = 0

    #         # Send the data!
    #         while len(fileData) > numSent:
    #             numSent += controlSocket.send(fileData[numSent:].encode("utf-8"))

    #     # The file has been read. We are done
    #     else:
    #         break

    # print("Sent ", numSent, " bytes.")

    # fileObj.close()


def list_files(controlSocket, serverAddress):
    print("before send")
    send_command(controlSocket, "ls")
    print("after send")


def main():
    serverAddress, serverPort = check_file_args()
    print(f"Creating control socket for {serverAddress}:{serverPort}")
    controlSocket = connect_to_server(serverAddress, serverPort)

    while True:
        command = input("Enter a command: ")
        if command not in ["get", "put", "ls", "quit", "help"]:
            print("Invalid command")
            print_command_help()
            continue

        if command == "help":
            print_command_help()
            continue
        elif command == "quit":
            break

        if command == "get":
            fileName = input("Enter a file name: ")
            get_file(controlSocket, serverAddress, fileName)
        elif command == "put":
            fileName = input("Enter a file name: ")
            put_file(controlSocket, serverAddress, fileName)
        elif command == "ls":
            list_files(controlSocket, serverAddress)

    controlSocket.close()


if __name__ == "__main__":
    main()
