#Universitat de Barcelona. Domotica
#2019
#Authors:
#         Arnau Vicente Puiggros - GitHub: @arnaudeveloper
#         Alvaro Baucells Costa

#Codi TIM


import utime
import network
import socket
import machine


def irq_up(up_pin):
    # wait for pin to change value
    # it needs to be stable for a continuous 20ms
    #utime.sleep_ms(50)
    global state
    state  = 'arriba'
    
    
def irq_down(down_pin):
    # wait for pin to change value
    # it needs to be stable for a continuous 20ms
    global state
    state  = 'abajo'
    
    
def irq_ok(ok_pin):
    # wait for pin to change value
    # it needs to be stable for a continuous 20ms
    #utime.sleep_ms(50)
    global press
    press=1
    
    
def irq_left(left_pin):
    # wait for pin to change value
    # it needs to be stable for a continuous 20ms
    #utime.sleep_ms(50)
    global state, state2, exit
    state  = 'izquierda'
    state2 = 'izquierda'
    exit=1
    
    
 
def irq_right(right_pin):
    # wait for pin to change value
    # it needs to be stable for a continuous 20ms
    #utime.sleep_ms(50)
    global state, state2
    state  = 'derecha'
    state2 = 'derecha'
    
def Enviem_ip_al_NCAP(ip,host,port):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     #Crea un socket

  s.connect((host,port))                                    #Ens connectem al port 2000 del NCAP (host)
  msg=ip                                                    #Creem un missatge amb la nostra ip, perque NCAP ens pogui identificar
  s.send(msg)                                               #Enviem el missatge pel port 
  data = s.recv(1024)                                       #Capturem la resposta del NCAP pel port 2000
  
  print("Data from NCAP:",data)                             #Printem la resposta
  
  s.close()                                                 #Tanquem el socket
  utime.sleep_ms(5000)                                      #Delay 


def Ens_conectem_a_la_red(ssid,password,station):
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










