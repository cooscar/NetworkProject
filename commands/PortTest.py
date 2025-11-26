import socket
import sys
import ipaddress



port = 0
ip = ""
ctype = ""
_max_tcp_conn = 20


class TcpSer:
    if __name__ == "__main__":


        def validip(tip):
            try:
                ipaddress.ip_address(tip)
                return True
            except ValueError:
                return False
            

        def validport(tport):
            try:

                port = int(tport)

                if (1 <= port <= 65535):
                    return True
                else:
                    return False
                
            except ValueError:
                return False
        
            
        if len(sys.argv) > 1:    
            for i in range(len(sys.argv)):
                value = sys.argv[i]


                if value == "-P" or value == "-p":
                    if (validport(sys.argv[i + 1])):
                        port = sys.argv[i + 1]
                    else:
                        print("The entered port is invalid")


                elif value == "-I" or value == "-i":
                    if (validip((sys.argv[i + 1]))):
                        ip = sys.argv[i + 1]
                    else:
                        print("The entered ip address is invalid")


                elif value == "-T" or value == "-t":
                    ctype = "TCP"
                elif value == "-U" or value == "-u":
                    ctype = "UDP" 

            if (ctype == "" or port == 0 or ip == ""):
                print("Please use the correct synthax: luma -I <ip> -P <port> -T {for TCP type connections} -U {for udp type connections}")
            else:
                pass
                
            

            def is_port_open(port, ip, type, timeout=2):
                port = int(port)
                type = str(type)

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(timeout)
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(timeout)
         
                if (type == "TCP"):
                    try:
                        s.connect((ip, port))
                        s.close
                        return True
                    except (socket.timeout, ConnectionRefusedError, OSError):
                        return False
                
                elif (type == "UDP"):
                    try:
                        sock.sendto(b"test", (ip, port))
                        sock.recvfrom(1024)  
                        return True          
                    except socket.timeout:
                        return False          
                    except ConnectionRefusedError:
                        return False
                        


            if (is_port_open(port, ip, ctype)):
                print("the port is open")
            else:
                print("unable to connect to the port")
           
                     

