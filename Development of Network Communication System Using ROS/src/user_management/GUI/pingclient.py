import socket
def pingsvc():
    # try to ping the master IP
    try:
        socket.setdefaulttimeout(1)
        # if we do not receive data for 1 second except will kick in

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # AF_INET: address family
        # SOCK_STREAM: type for TCP

        host = "192.168.247.27" #OCS
        port = 11311

        server_address = (host, port)
        soc.connect(server_address)

    except OSError as error:
        print('Err')
        return False
        # function returns false value
        # disconnection is detected

    else:
        print('OK')
        soc.close()
        # closing the connection after the
        # communication with the master is complete
        return True
ping_ocs()