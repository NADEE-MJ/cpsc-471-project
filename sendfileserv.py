import sys
import os

from utils.protocol import receive_data, send_data
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

            if command == "get":
                pass
                # get_file(clientSock, command_list[1])
            elif command == "put":
                pass
                # send_file(clientSock, command_list[1])
            elif command == "ls":
                send_ls(client_socket, client_address, data_socket_port)
            elif command == "help":
                print_command_help()
            elif command == "quit":
                print("Closing connection...")
                client_socket.close()
                break
            else:
                print("Invalid command")


if __name__ == "__main__":
    main()
