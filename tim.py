
#Universitat de Barcelona. Domotica
#2019
#Authors:
#         Arnau Vicente Puiggros - GitHub: @arnaudeveloper
#         Alvaro Baucells Costa

#Codi TIM

import network
import machine
import socket
import utime

import struct

#---Variables-----------------------------------------------

host='192.168.4.1'                                          #necesitem ip del NCAP, que al primer socket actua com a servidor (host) 
port=2000                                                   #port del primer socket
s=None
data=''
ssid = 'NCAP'                                               #dades de la xarxa del NCAP
password = 'esp32ibz'

#---Funcions------------------------------------------------

def Enviem_ip_al_NCAP(ip):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     #Crea un socket

  s.connect((host,port))                                    #Ens connectem al port 2000 del NCAP (host)
  msg=ip                                                    #Creem un missatge amb la nostra ip, perque NCAP ens pogui identificar
  s.send(msg)                                               #Enviem el missatge pel port 
  data = s.recv(1024)                                       #Capturem la resposta del NCAP pel port 2000
  
  print("Data from NCAP:",data)                             #Printem la resposta
  
  s.close()                                                 #Tanquem el socket
  utime.sleep_ms(5000)                                      #Delay 


def Ens_conectem_a_la_red(ssid,password):
  station.connect(ssid, password)                           #Connecta amb el ssid i el passwd

  while station.isconnected() == False:
    pass

  print('Connection successful')
  print(station.ifconfig())
  
def Analitzar_comanda(request):
  if request==128:
    comanda="Llegir"
  elif request==160:
    comanda="Llegir TEDS"
  elif request==3:
    comanda="Definir canal trigger"
  elif request==255:
    comanda="Trigger"
  elif request==0:
    comanda="Escriure"
  else:
    comanda="NO WORK"
  return comanda
  

#---Codi---------------------------------------------------

station = network.WLAN(network.STA_IF)          #el TIM el configurem com a estacio, que accedeix a la xarxa del NCAP
station.active(True)                            
Ens_conectem_a_la_red(ssid,password)


try:
  
  ip=station.ifconfig()[0]                      #agafem la nostra ip per obrir el segon socket (ara com servidor)
  print('ip:', ip)
  
  Enviem_ip_al_NCAP(ip)

  
  #Configuracio del segon socket com a servidor
  
  s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Es crea el segon socket (utilitzarem port 2005)
  s2.bind((ip,2005))                                      #Enllecem la nostra ip amb el socket que obrirem per escoltar (Servidor)
  s2.listen(5)                                            #Limit de requests que acceptara

  while True:
    
    conn, addr = s2.accept()         #estableix connexio quan rep un request, i guarda la direccio del client
    print('Got a connection from %s' % str(addr))

    request = conn.recv(1024)        #rep missatge del client, amb un limit de 1024 bytes
    #Rebem la instruccio en bytes unpack    
    #request = str(request)    
    #print('Content = %s' % request)  #Printa tot el que ha capturat
    
    recuperem_variable=struct.unpack('h',request)    #Perfect
    
    comanda = recuperem_variable[0]
    print(comanda)

    
    #request=request.split("'")[1]  
    num_de_funcio=Analitzar_comanda(comanda)
    print("Num de funcio: ",num_de_funcio)

    
    response = "DATA"                #missatge que li tornem al client (en funcio del que demani)
    #Enviem la resposta en bytes pack
    conn.sendall(response)           #Enviem la resposta
    conn.close()                     #Tanquem connexio per esperar la seguent connexio (es crea a l'inici del while)
      
    
except:                              #si es para el programa de manera externa, s'ha de tancar el socket
  if (s2):    
    s2.close()                       #si esta obert el socket, el tanca per evitar problemes a l'hora de tornar-lo a obrir en un futur
  station.disconnect()               #si s'ha parat el programa, es desconecta de la xarxa
  station.active(False)



