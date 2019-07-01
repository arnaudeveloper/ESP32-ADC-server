


#Universitat de Barcelona. Domotica
#2019
#Authors:
#         Alvaro Baucells Costa  
#         Arnau Vicente Puiggros - GitHub: @arnaudeveloper

import network
import machine
import socket
import utime
import struct

s=None
data=''
essid='NCAP'
password='esp32ibz'

def init():
  global TIM1_NAME
  global Channel1_TIM1_NAME
  global Units_Channel1_TIM1_NAME
  global Value_Channel1_TIM1_NAME
  global Channel2_TIM1_NAME
  global Units_Channel2_TIM1_NAME
  global Value_Channel2_TIM1_NAME
  global TIM2_NAME
  global Channel1_TIM2_NAME
  global Units_Channel1_TIM2_NAME
  global Value_Channel1_TIM2_NAME
  global Channel2_TIM2_NAME
  global Units_Channel2_TIM2_NAME
  global Value_Channel2_TIM2_NAME

  TIM1_NAME="TIM1_NAME"
  Channel1_TIM1_NAME="NAME1"
  Units_Channel1_TIM1_NAME="NAME1"
  Value_Channel1_TIM1_NAME="NAME1"
  Channel2_TIM1_NAME="NAME1"
  Units_Channel2_TIM1_NAME="NAME1"
  Value_Channel2_TIM1_NAME="NAME1"
  TIM2_NAME="NAME1"
  Channel1_TIM2_NAME="NAME1"
  Units_Channel1_TIM2_NAME="NAME1"
  Value_Channel1_TIM2_NAME="NAME1"
  Channel2_TIM2_NAME="NAME1"
  Units_Channel2_TIM2_NAME="NAME1"

  Value_Channel2_TIM2_NAME="NAME1"

def web_page():
  html = """
  <html>
    <head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,">
      <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
    				h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}
        			.button{display: inline-block; background-color: #e7bd3b; border: none;border-radius: 4px; color:white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: 									pointer;}
    				.button2{background-color: #0000FF;}
       				.button3{background-color: #FF0000;}
      </style>
    </head>
    <body> <h1>ESP Web Server</h1>
	<h2 style="text-align: center;">Tim 1: """+TIM1_NAME+""" <a href="/?led=TIM1"><button class="button">READ</button></a></h2> 
	<ul>
	<li style="text-align: center;">Channel 1: """+Channel1_TIM1_NAME +"""
	<ul>
	<li style="text-align: center;">Units: """+Units_Channel1_TIM1_NAME+"""</li>
	<li style="text-align: center;">Value: """+Value_Channel1_TIM1_NAME+"""</li>
	</ul>
	</li>
	</ul>
	<ul>
	<li style="text-align: center;">Channel 2: """+Channel2_TIM1_NAME+""" 
	<ul>
	<li style="text-align: center;">Units: """+Units_Channel2_TIM1_NAME+"""</li>
	<li style="text-align: center;">Value: """+Value_Channel2_TIM1_NAME+"""</li>
	</ul>
	</li>
	</ul>
	<h2 style="text-align: center;">Tim 2: """+TIM2_NAME+""" <a href="/?led=TIM2"><button class="button button3">READ</button></a></h2>
	<ul>
	<li style="text-align: center;">Channel 1: """+Channel1_TIM2_NAME+"""
	<ul>
	<li style="text-align: center;">Units: """+Units_Channel1_TIM2_NAME+"""</li>
	<li style="text-align: center;">Value: """+Value_Channel1_TIM2_NAME+"""</li>
	</ul>
	</li>
	</ul>
	<ul>
	<li style="text-align: center;">Channel 2: """+Channel2_TIM2_NAME+"""
	<ul>
	<li style="text-align: center;">Units: """+Units_Channel2_TIM2_NAME+"""</li>
	<li style="text-align: center;">Value: """+Value_Channel2_TIM2_NAME+"""</li>
	</ul>
	</li>
	</ul>
           
      <h1>Send Function</h1>
      <form action='wifi.py' method='get'>
        <label for="myname">Command input</label>
        <input id="myname" type="text" name="firstname" value="write your command" />
        <input type="submit">
      </form>
    </body>
  </html>
  """
  return html

def Configuracio_acces_point(essid,password):
  global ap
  ap = network.WLAN(network.AP_IF)                                        #Configurem l'ESP32 com Acces Point
  ap.active(True)                                                         #Activem l'Acces Point
  ap.config(essid=essid, authmode=network.AUTH_WPA_WPA2_PSK, password=password)          #Configurem l'Acces Point. SSID+ PASSWD               
  
  print(ap.active())                                                      #Printar l'estat
  print(ap.ifconfig())                                                    #Printar la configuracio

def Envia_comanda_al_TIM(ip_TIM,msg):
  p2=2005                                                     #Port per on l'NCAP fa les seves comandes
  #msg='hola servidor'                                       #Comanda


  print('iniciem config client')

  #addr_info = socket.getaddrinfo("towel.blinkenlights.nl", 23)          #MAGIC!
  #print(addr_info)                                                      #MAGIC!


  #s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)         #Creem un socket
  #s.close()                                                   #Tanquem el socket

  utime.sleep_ms(5000)                                        #Delay
  
  s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #Creem el socket

  s.connect((ip_TIM, p2))                                   #Ens connectem al socket

  print('antes', msg)
 
  s.send(msg)                                               #Enviem la comanda
  print ('despues')
  data=s.recv(1024)                                         #Capturem la resposta
  #print(data)                                               #Printem la resposta
  if decode==1:
    data=struct.unpack('f', data)
    print('data float',data)
  elif decode==0:
    #data=struct.unpack('ffffffffffff', data)
    print('data TEDS',data)
  else:
    print(data) 
  s.close()                                                 #Tanquem la connexio
  utime.sleep_ms(2000)                                      #Delay
  
  return data


  


 
 
 
#---Code----
#-----------------

init()    #inici varaibles

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
    print("DEBUG============>")
    s.close() 


#A partir d'aquest punt l'NCAP tanca el socket 2000, i  actua com a client


'''s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip, 80))
s.listen(5)'''

try:
  j=0
  inf=0
  decode=10
  while True:

  
    '''conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
  
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)  #Printa tot el que ha capturat
    
    if 'firstname' in request:
      name = request.split('=')[1]
    else:
      name = 'No name'
      
    #Afegint box funciona??
  
    #second_value_html = request.find('/?firstname')
    #second_value_html = request.find('/?value')
  
  
    #name = value_html.split('=')[1]
    print('Aqui va el que he capturat----->>>')
    #print(second_value_html)
    msg=name.split()[0]
    print(name.split()[0])
    
  
  
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()'''
    #debug
    if j==0:

      msg=160
      decode=0
      
    
    if j==1:
      msg=255
      #msg=3
      inf=2
      decode=1
      
    if j==2:
      msg=0
      inf=255
      decode=1
      
    if j==3:
      msg=128
      decode=1
      
    if j==4:
      #msg=255
      msg=3
      decode=1
      j=-1
      
    #env=struct.pack('h', msg)
    env=struct.pack('hh', msg, inf)
    
    
    Envia_comanda_al_TIM(ip_TIM,env)
    j=j+1
    
   
except:
  if (s):    
    s.close()                       #si esta obert el socket, el tanca per evitar problemes a l'hora de tornar-lo a obrir en un futur
  ap.disconnect()               #si s'ha parat el programa, es desconecta de la xarxa
  ap.active(False)
    


