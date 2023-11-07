import socket


def connect_to_socket(server_address, server_port):
    """
    Connects to a socket.

    Parameters:
        server_address (str): the server address
        server_port (int): the server port number

    Returns:
        connection_socket (socket): the connection socket
    """
    # Create a TCP socket
    connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    connection_socket.connect((server_address, server_port))

    return connection_socket


def create_control_socket_server(server_port):
    """
    Creates a control socket server.

    Parameters:
        server_port (int): the port number to bind to

    Returns:
        welcome_socket (socket): the welcome socket
    """
    # Create a welcome socket.
    welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    welcome_socket.bind(("", server_port))

    return welcome_socket


def create_ephemeral_socket_server():
    """
    Creates an ephemeral socket server.

    Returns:
        welcome_socket (socket): the welcome socket
        ephemeral_port (int): the ephemeral port number
    """
    # Create a welcome socket.
    welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to port 0
    welcome_socket.bind(("", 0))

    # Retrieve the ephemeral port number
    ephemeral_port = welcome_socket.getsockname()[1]

    return welcome_socket, ephemeral_port
