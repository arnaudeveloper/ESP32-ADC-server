
import network
import machine
import socket
import utime

host='192.168.4.1'
port=2000
s=None
data=''


ssid = 'NCAP'
password = 'esp32ibz'

def Enviem_ip_al_NCAP(ip):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     #Crea un socket

  s.connect((host,port))                                    #Ens connectem al port 2000 del NCAP (host)
  
  msg=ip                                                    #Creem unmissatge amb la nostra ip
  print("DEBUG===================>>>")
  s.send(msg)                                               #Enviem el missatge pel port 
  print("DEBUG===================>>>")

  data = s.recv(1024)                                       #Capturem la resposta del NCAP pel port 2000
  
  
  print("Data from NCAP:",data)                              #Prinetm la resposta
  
  s.close()                                                 #Tanquem el socket
  
  utime.sleep_ms(5000)                                      #Delay


def Ens_conectem_a_la_red(ssid,password):
  station.connect(ssid, password)                         #Connecta amb el ssid i el passwd

  while station.isconnected() == False:
    pass

  print('Connection successful')
  print(station.ifconfig())
  


#---Codi-----
#-------
station = network.WLAN(network.STA_IF)

station.active(True)

Ens_conectem_a_la_red(ssid,password)


try:
  
  ip=station.ifconfig()[0]                                 #get ip addr
  
  print('ip:', ip)
  
  Enviem_ip_al_NCAP(ip)

  #Configurem_el_socket_com_servidor(ip,port=2001)
  #Configuraci
  s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Socket del port 20001. Servidor
  
  s2.bind((ip,2001))                                      #Enllecem la nostra ip amb el socket que obrirem per escoltar (Servidor)
  s2.listen(5)                                            #Limit de clients

  while True:
    
    conn, addr = s2.accept()
    print('Got a connection from %s' % str(addr))

    request = conn.recv(1024)
    request = str(request)
    #Analitzar el request
    ###
    
    ###
    print('Content = %s' % request)  #Printa tot el que ha capturat
    
    #En funcio del request contestem
    response = "DATA"     #dades que ens ha demenat
    
    conn.sendall(response)#Enviem la resposta
    conn.close()#Tanquem connexio per esperar a la seguent
      
    
except:
  if (s2):
    s2.close()
  
  station.disconnect()
  station.active(False)








