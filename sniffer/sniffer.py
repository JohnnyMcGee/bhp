import socket
import os

# host to listen on
HOST = '127.0.0.1'

def main():
    # create raw socket, bin to public interface
    windows = os.name == 'nt'
    if windows:
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP
    
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((HOST, 0))

    # include the IP header in the capture
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    if windows:
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    
    # read one packet
    print(sniffer.recvfrom(65565))

    if windows:
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)


if __name__ == '__main__':
    main()