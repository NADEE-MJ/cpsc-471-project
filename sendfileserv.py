import sys
import os

from utils.protocol import receive_data, send_data, check_file_exists
from utils.socket import connect_to_socket, create_control_socket_server


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

    server_port = int(sys.argv[1]) if len(sys.argv) >= 2 else 1234

    return server_port


def send_ls(control_socket, client_address, data_socket_port):
    data_socket = connect_to_socket(client_address, data_socket_port)
    try:
        files = os.listdir("ftp/")
        files = "\n".join(files)
    except Exception as e:
        print(e)
        send_data(data_socket, "1", flag=1)
        send_data(control_socket, "Something went wrong")
    else:
        send_data(data_socket, files)
    finally:
        data_socket.close()


def send_file(control_socket, client_sock, file_name, data_socket_port):
    if not check_file_exists(file_name):
        print("File doesnt exist")
        send_data(client_sock, "", data_socket_port, 2)
        send_data(control_socket, "Files doesnt exist")

    file = open("ftp/" + file_name, "r")
    file_data = file.read()
    send_data(client_sock, file_data, data_socket_port)
    file.close()


def main():
    server_port = check_file_args()
    control_socket = create_control_socket_server(server_port)

    # Start listening on the socket
    control_socket.listen(1)

    while True:
        print("Waiting for connections...")

        client_socket, client_info = control_socket.accept()
        client_address = client_info[0]
        client_port = client_info[1]
        print(f"Accepted connection from client: {client_address}:{client_port}")
        print("\n")

        while True:
            command, data_socket_port = receive_data(client_socket)
            command_list = command.split(" ", 1)

            print(command_list)
            if command_list[0] == "get":
                send_file(control_socket, client_socket, command_list[1], data_socket_port)
                print("File sent")
            elif command_list[0] == "put":
                pass
                # send_file(clientSock, command_list[1])
            elif command_list[0] == "ls":
                send_ls(client_socket, client_address, data_socket_port)
            elif command_list[0] == "help":
                print_command_help()
            elif command_list[0] == "quit":
                print("Closing connection...")
                client_socket.close()
                break
            else:
                print("Invalid command")


if __name__ == "__main__":
    main()
