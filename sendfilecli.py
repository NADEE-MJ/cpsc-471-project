import os
import sys
from utils.protocol import send_data, receive_data, decode_header
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

    serverAddress = sys.argv[1] if len(sys.argv) > 1 else "localhost"

    serverPort = int(sys.argv[2]) if len(sys.argv) > 2 else 1234

    return serverAddress, serverPort


#ls command
def list_files(control_socket):
    data_socket, data_socket_port = create_ephemeral_socket_server()
    data_socket.listen(1)
    send_data(control_socket, "ls", data_socket_port)

    data_socket, data_socket_address = data_socket.accept()
    data, port = receive_data(data_socket)
    if data is None:
        # there was an error
        data, port = receive_data(control_socket)
        print(data)
    else:
        print(data)

    data_socket.close()


#get command
def get_file(control_socket, file_name):
    data_socket, data_socket_port = create_ephemeral_socket_server()
    data_socket.listen(1)
    send_data(control_socket, "get " + file_name, data_socket_port)

    data_socket, data_socket_address = data_socket.accept()
    data, port = receive_data(data_socket)
    if data is None:
        data, port = receive_data(control_socket)
        #print(data)
    else:
        print("Received: " + file_name + " of size " + str(len(data)) + " bytes")
        with open("client_files/" + file_name, "w") as new_file:
            new_file.write(data)
        print(file_name + " was successfully written")
    data_socket.close()


#put command
def put_file(control_socket, file_name, server_file_name):
    if not os.path.exists("client_files/" + file_name):
        print("File could not be found to send to server, please try again")
        return
    data_socket, data_socket_port = create_ephemeral_socket_server()
    data_socket.listen(1)
    send_data(control_socket, "put " + server_file_name, data_socket_port)
    
    data_socket, data_socket_address = data_socket.accept()
    data, port = receive_data(data_socket)
    if data is None:
        _, _, flag = decode_header(data)
        if flag == 2:
            print("unable to create put file")
        data, port = receive_data(control_socket)
    else:
        print("Server is ready for file transmission")
        #print(data)
    
    
    with open("client_files/" + file_name, "r") as file:
        file_data = file.read()
    send_data(data_socket, file_data, data_socket_port)
    
    print("Data is fully in transmission to server")
    data, port = receive_data(control_socket)
    if data is not None or "3":
        print("Data has been successfully received by server")
    


def main():
    serverAddress, serverPort = check_file_args()

    print(f"Creating control socket for {serverAddress}:{serverPort}")
    control_socket = None
    try:
        control_socket = connect_to_socket(serverAddress, serverPort)
    except ConnectionRefusedError as e:
        print("Could not connect to server. Are you sure you have the right server address and port number?\n" + str(e))
        exit()
    
    while True:
        command = input("ftp> ")
        command_list = command.split(" ", 1)
        if command_list[0] not in ["get", "put", "ls", "quit", "help"]:
            print("Invalid command")
            print_command_help()
            continue

        if command_list[0] == "help":
            print_command_help()
            continue
        elif command_list[0] == "quit":
            print("Closing connection...")
            send_data(control_socket, "quit")
            break
        elif command_list[0] == "get":
            file_name = command_list[1]
            get_file(control_socket, file_name)
        elif command_list[0] == "put":
            file_name = command_list[1]
            server_file_name = input("Enter the name for the file on the server, press enter to keep same: ")
            print()
            if server_file_name == str():
                server_file_name = file_name
            put_file(control_socket, file_name, server_file_name)
        elif command_list[0] == "ls":
            list_files(control_socket)

    control_socket.close()


if __name__ == "__main__":
    main()
