
# esp32 ACCES POINT + SERVER

import network

try:
  import usocket as socket
except:
  import socket

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='RED_PEPE', authmode=network.AUTH_WPA_WPA2_PSK, password='12345678')
ap.ifconfig(('192.168.84.1', '255.255.255.0', '192.168.84.1', '192.168.84.1')) # ip, netmask, gateway, dns

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #Creem el socket
s.bind((ap.ifconfig()[0], 80))
#s.bind((ip, 80))

s.listen(5)

try:
  while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    #pass
    
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)  #Printa tot el que ha capturat
    
    response="OK"
    
    conn.sendall(response)
    
    
    conn.close()  #Tanca la connexio
    
except:
  ap.disconnect()
  



