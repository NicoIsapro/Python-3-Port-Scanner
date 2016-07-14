
                     #-------------------------------------------------------------------------------#
                     #                         Range Client Scanner Port                             #
                     #-------------------------------------------------------------------------------#
				   
import socket
import sys
import os 

os.system('color A')      # Couleur du programme (Facultatif)
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

# Nettoyage d'écran (Facultatif)
cls()

# Variables de départ
tcp = 1
verbose = 0
fichier = open("exemple.txt", "w")  # Nom du fichier à utiliser

def main():

    # Bloc d'IP
    targets = returnCIDR('193.178.154.0/24') 

    # Port à utiliser 
    ports = [80] 


    # Scan
    for target in targets:
        tcpports = portscan(target,ports)

def portscan(target,ports):

    printmsg("Scan des IP en cours ")
    tcpports=[]
    if tcp:
        for portnum in ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.04)
                s.connect((target, portnum))
            except Exception:
                failvar = 0
                if verbose: print ("%d/tcp \tclosed" % (portnum))
            else:
                tcpports.append(portnum)
            s.close()
    if len(tcpports) == 1:                                        # Si il détecte un port il l'écrit dans le fichier
           printmsg(("IP trouvé :  %s" % (target)))
           fichier.write("\n"+target)                             # /n pour le saut de ligne des IP 
           		   

def printmsg(msg): print ("[+] Scanner: %s" % (msg))


def iprange(addressrange): # converts a ip range into a list
    list=[]
    first3octets = '.'.join(addressrange.split('-')[0].split('.')[:3]) + '.'
    for i in range(int(addressrange.split('-')[0].split('.')[3]),int(addressrange.split('-')[1])+1):
        list.append(first3octets+str(i))
    return list

def ip2bin(ip):
    b = ""
    inQuads = ip.split(".")
    outQuads = 4
    for q in inQuads:
        if q != "": b += dec2bin(int(q),8); outQuads -= 1
    while outQuads > 0: b += "00000000"; outQuads -= 1
    return b

def dec2bin(n,d=None):
    s = ""
    while n>0:
        if n&1: s = "1"+s
        else: s = "0"+s
        n >>= 1
    if d is not None:
        while len(s)<d: s = "0"+s
    if s == "": s = "0"
    return s

def bin2ip(b):
    ip = ""
    for i in range(0,len(b),8):
        ip += str(int(b[i:i+8],2))+"."
    return ip[:-1]

def returnCIDR(c):
    parts = c.split("/")
    baseIP = ip2bin(parts[0])
    subnet = int(parts[1])
    ips=[]
    if subnet == 32: return bin2ip(baseIP)
    else:
        ipPrefix = baseIP[:-(32-subnet)]
        for i in range(2**(32-subnet)): ips.append(bin2ip(ipPrefix+dec2bin(i, (32-subnet))))
        return ips

if __name__ == '__main__':
    main()