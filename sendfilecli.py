import os
import sys
from utils.protocol import send_data
from utils.socket import connect_to_socket, create_ephemeral_socket_server


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


def get_file(control_socket, serverAddress, fileName):
    print("Receiving file...")
    #! WRITE CODE FOR RECEIVING FILE
    # control_socket.send(command.encode("utf-8"))
    # control_socket.send(fileName.encode("utf-8"))
    # fileObj = open(fileName, "w")
    # while True:
    #     data = control_socket.recv(1024).decode("utf-8")
    #     if not data:
    #         break
    #     fileObj.write(data)
    # fileObj.close()


def put_file(control_socket, serverAddress, fileName):
    if not os.path.isfile(fileName):
        print("File does not exist")

    #! WRITE CODE FOR SENDING FILE
    # control_socket.send(command.encode("utf-8"))
    # control_socket.send(fileName.encode("utf-8"))
    # print("Sending file...")
    # put_file(control_socket, fileName)
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
    #         data_size_str = str(len(fileData))

    #         # Prepend 0's to the size string
    #         # until the size is 10 bytes
    #         while len(data_size_str) < 10:
    #             data_size_str = "0" + data_size_str

    #         # Prepend the size of the data to the
    #         # file data.
    #         fileData = data_size_str + fileData

    #         # The number of bytes sent
    #         numSent = 0

    #         # Send the data!
    #         while len(fileData) > numSent:
    #             numSent += control_socket.send(fileData[numSent:].encode("utf-8"))

    #     # The file has been read. We are done
    #     else:
    #         break

    # print("Sent ", numSent, " bytes.")

    # fileObj.close()


def list_files(control_socket):
    print("Opening data socket")
    data_socket, data_socket_port = create_ephemeral_socket_server()
    data_socket.listen(1)
    send_data(control_socket, "ls", data_socket_port)

    data_socket, data_socket_address = data_socket.accept()
    print(data_socket.recv(1024).decode("utf-8"))
    data_socket.close()


def main():
    serverAddress, serverPort = check_file_args()

    print(f"Creating control socket for {serverAddress}:{serverPort}")
    control_socket = connect_to_socket(serverAddress, serverPort)

    while True:
        command = input("ftp> ")
        if command not in ["get", "put", "ls", "quit", "help"]:
            print("Invalid command")
            print_command_help()
            continue

        if command == "help":
            print_command_help()
            continue
        elif command == "quit":
            print("Closing connection...")
            send_data(control_socket, "quit")
            break
        elif command == "get":
            fileName = input("Enter a file name: ")
            get_file(control_socket, fileName)
        elif command == "put":
            fileName = input("Enter a file name: ")
            put_file(control_socket, fileName)
        elif command == "ls":
            list_files(control_socket)

    control_socket.close()


if __name__ == "__main__":
    main()
