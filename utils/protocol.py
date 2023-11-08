PROTOCOL_HEADER_LENGTH = 16


def create_protocol_header(content, data_socket_port):
    """
    Creates a header for the protocol

    The header is in the format:
    <length of content>:<data socket port>

    Length of the header is 16 bytes

    Parameters:
        content (str): the content to be sent
        data_socket_port (int): the port number of the data socket

    Returns:
        str: the header
    """
    header = f"{len(content):010d}:{data_socket_port:05d}"
    return header


def decode_header(header):
    split_header = header.split(":")
    content_length = int(split_header[0])
    data_socket_port = int(split_header[1])
    return content_length, data_socket_port


def receive_bytes_from_socket(sock, num_bytes):
    """
    Receives the specified number of bytes from the specified socket

    Parameters:
        sock (socket): the socket from which to receive
        num_bytes (int): the number of bytes to receive

    Returns:
        bytes: the bytes received
    """
    main_buffer = b""

    temp_buffer = b""

    # Keep receiving till num_bytes bytes is received
    while len(main_buffer) < num_bytes:
        # Attempt to receive bytes
        temp_buffer = sock.recv(num_bytes)

        # The other side has closed the socket
        if not temp_buffer:
            break

        main_buffer += temp_buffer

    return main_buffer


def receive_data(sock):
    header = receive_bytes_from_socket(sock, PROTOCOL_HEADER_LENGTH).decode("utf-8")
    print(header)
    content_length, data_socket_port = decode_header(header)

    data = receive_bytes_from_socket(sock, content_length).decode("utf-8")

    return data, data_socket_port


def send_data(sock, data, data_socket_port=0):
    header = create_protocol_header(data, data_socket_port)

    data = header + data

    # send the data in packets of length PROTOCOL_PACKET_LENGTH
    bytes_sent = 0

    while len(data) > bytes_sent:
        bytes_sent += sock.send(data[bytes_sent:].encode("utf-8"))

    return bytes_sent
