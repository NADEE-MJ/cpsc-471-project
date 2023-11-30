# CPSC-471 Final Project

## Group Members

- Nadeem Maida - nmaida@csu.fullerton.edu
- Nathan Storm - nathanstorm95@csu.fullerton.edu
- Jake Watson  -  jrwatson@csu.fullerton.edu

Programming language: Python

## How to run :rocket:

1. **Run the server:**
   `python3 sendfileserv.py [server port]`
2. **Run the client:**
   `python3 sendfilecli.py [server address] [server port]`

Note: the command line arguments are optional:

### Server

- server port: the port the server will listen on, default is `1234`
- add the -h or --help flag when running the server file for more information

### Client

- server address: the address of the server, default is localhost
- server port: the port the server is listening on, default is `1234`
- add the -h or --help flag when running the client file for more information

Client's files are stored in the client_files directory, server files are in the ftp directory.

### Client CLI

The main options while using the client cli are:

- `get [filename]` - download a file from the server
- `put [filename]` - upload a file to the server
- `ls` - list the files available to download from the server
- `quit` - exit the cli and disconnect from the server
- `help` - display the help menu

For information on the available commands in the cli, run the client with `python3 sendfilecli.py`, and then type `help`. Otherwise, reference the programming assignment PDF on Canvas.
