#Universitat de Barcelona. Domotica
#2019
#Authors:
#         Alvaro Baucells Costa  
#         Arnau Vicente Puiggros - GitHub: @arnaudeveloper

import network
import machine
import socket
import utime


s=None
data=''
essid='NCAP'
password='esp32ibz'

def Configuracio_acces_point(essid,password):
  global ap
  ap = network.WLAN(network.AP_IF)                                        #Configurem l'ESP32 com Acces Point
  ap.active(True)                                                         #Activem l'Acces Point
  ap.config(essid=essid, authmode=network.AUTH_WPA_WPA2_PSK, password=password)          #Configurem l'Acces Point. SSID+ PASSWD               
  
  print(ap.active())                                                      #Printar l'estat
  print(ap.ifconfig())                                                    #Printar la configuracio


 #Codi------------
 #-----------
 
 
 
#---Code----
#-----------------
Configuracio_acces_point(essid,password)                  #Configurem l'NCAP com Acces Point


ip=ap.ifconfig()[0]                                         #Obtenim la IP propia
port=2000                                                   #Port que utilitzarem per rebre les dades dels TIMs

#Configuracio_del_socket_server(ip,port)  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #Creem un socket
s.bind((ip,port))                                           #Enllecem la ip amb el  port
s.listen(5)                                                 #Numero maxim de clients, simultanis

count=0                                                     #Variable que ens serveix per contar el num de TIMs connectats

while count<1:            #Aquest while estara actiu fins que tots els TIMs s'han connectat
  
  conn, addr = s.accept()                                   #Crea una connexio quan el client envia un request
  print('Got a connection from %s' % str(addr))
  
  request = conn.recv(1024)                                 #Capturem el missatge del client
  request = str(request)                                    #Ho convertim a string
  print('Content = %s' % request)                           #Printem el missatge
  
  utime.sleep_ms(500)                                       #Delay
  
  ip_TIM=request.split("'")[1]                              #Separem la IP del TIM
  print('ip del tim:', ip_TIM)
  
  response = ip_TIM + '+ ok'                                #Creem la reposta
  conn.sendall(response)                                    #Enviem la resposta
  
  conn.close()                                              #Tanquem la connexio 
  
  count=count+1                                             #Contador de ESP connectats
  print('count',count)                                      #Printem el num. de TIMs connectats
  
  if count==1:                                              #Si hem arribat al limit de connexions tanquem el socket
    s.close() 


#A partir d'aquest punt l'NCAP tanca el socket 2000, i  actua com a client

print('iniciem config client')

addr_info = socket.getaddrinfo("towel.blinkenlights.nl", 23)          #MAGIC!
print(addr_info)                                                      #MAGIC!

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)         #Creem un socket
s.close()                                                   #Tanquem el socket

utime.sleep_ms(5000)                                        #Delay


p2=2005                                                     #Port per on l'NCAP fa les seves comandes


while True:
  s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #Creem el socket

  s.connect((ip_TIM, p2))                                   #Ens connectem al socket

  
  msg='hola servidor'                                       #Comanda
  s.send(msg)                                               #Enviem la comanda

  data=s.recv(1024)                                         #Capturem la resposta
  print(data)                                               #Printem la resposta 
  s.close()                                                 #Tanquem la connexio
  utime.sleep_ms(5000)                                      #Delay
    



 

