import sys
import os

from utils.protocol import receive_data, send_data, check_file_exists
from utils.socket import connect_to_socket, create_control_socket_server


DEFAULT_FILE_NAME = "error_file.txt"


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


#ls command
def send_ls(client_ssocket, client_address, data_socket_port):
    data_socket = connect_to_socket(client_address, data_socket_port)
    try:
        files = [
            f for f in os.listdir("ftp/") if os.path.isfile(os.path.join("ftp/", f))
        ]

        if not files:
            ls_text = "No files found in the specified folder."
        else:
            ls_text = f"{'#':<5} {'File Name'}\n"
            ls_text += "-" * 30 + "\n"

        for index, file_name in enumerate(files, start=1):
            ls_text += f"{index:<5} {file_name}\n"
    except Exception as e:
        print(e)
        send_data(data_socket, "1", flag=1)
        send_data(client_socket, "Something went wrong")
    else:
        send_data(data_socket, ls_text)
    finally:
        data_socket.close()


#get command
def send_file(client_socket, client_address, file_name, data_socket_port):
    data_socket = connect_to_socket(client_address, data_socket_port)
    if not check_file_exists(file_name):
        print("File does not exist")
        send_data(data_socket, "", data_socket_port, 2)
        send_data(client_socket, "File does not exist")
        return

    with open("ftp/" + file_name, "r") as file:
        file_data = file.read()
    send_data(data_socket, file_data, data_socket_port)
    print("File sent")


#put command
#the command is put, but the function is a 'get' since the file is received by the server
def get_file(client_socket, client_address, file_name, data_socket_port):
    data_socket = connect_to_socket(client_address, data_socket_port)
    send_data(data_socket, "R", data_socket_port, 0)
    data, port = receive_data(data_socket)
    
    print("Fully received " + file_name + " of size " + str(len(data)) + " bytes")
    try:
        with open("ftp/" + file_name, "w+") as f:
            f.write(data)
    except FileNotFoundError as e:
        print("No such file directory can be found, writing data to " + DEFAULT_FILE_NAME)
        send_data(client_socket, "", flag=2)
        with open("ftp/" + DEFAULT_FILE_NAME, "w+") as f:
            f.write(data)
        return
    print(file_name + " was successfully written")
    send_data(client_socket, "3", flag=3)
    print("Client notified that transmission is complete")

def main():
    server_port = check_file_args()
    control_socket = None
    try:
        control_socket = create_control_socket_server(server_port)
    except OSError as e:
        print("The server port is already in use. If you ran the server on the same port recently, please wait up to 30 seconds for the port to become available again\n" + str(e))
        exit()
    
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
                send_file(client_socket, client_address, command_list[1], data_socket_port)
            elif command_list[0] == "put":
                get_file(client_socket, client_address, command_list[1], data_socket_port)
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
    control_socket.close()

if __name__ == "__main__":
    main()
