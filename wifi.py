
# Complete project details at https://RandomNerdTutorials.com

#wifi
import network                            ##Llibreria

import os

try:
  import usocket as socket
except:
  import socket
  
from machine import Pin

import esp
#esp.osdebug(None)

import gc
gc.collect()


def web_page():
  gpio_state="OFF"
  
  html = """
  <html>
    <head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,">
      <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
    h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
    border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
    .button2{background-color: #4286f4;}
      </style>
    </head>
    <body> <h1>ESP Web Server</h1> 
      <p>GPIO state: <strong>""" + gpio_state + """</strong></p><p><a href="/?led=on"><button class="button">ON</button></a></p>
      <p><a href="/?led=off"><button class="button button2">OFF</button></a></p>      
      <h1>Form Demo</h1>
      <form action='wifi.py' method='get'>
        <label for="myname">Command input</label>
        <input id="myname" type="text" name="firstname" value="write your command" />
        <input type="submit">
      </form>
    </body>
  </html>
  """
  return html

  

station = network.WLAN(network.STA_IF)    ##Creem una estacio, dispositiu que es pot connectar a una red
station.active(True)                      ##Activem l'estacio

station.connect("death-note", "C@BRONES!miWIFI!") ##Usuari i contrasenya de la red

station.isconnected()                     ## Ens retorna si la conexio s'ha relaitzat
station.ifconfig()                        ## Ens retorna la configuracio de la connexio
ip=station.ifconfig()[0]

print('end wifi')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip, 80))
s.listen(5)

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))

  request = conn.recv(1024)
  request = str(request)
  #print('Content = %s' % request)  #Printa tot el que ha capturat
  
  if 'firstname' in request:
    name = request.split('=')[1]
  else:
    name = 'No name'

  #second_value_html = request.find('/?firstname')
  #second_value_html = request.find('/?value')


  #name = value_html.split('=')[1]
  print('Aqui va el que he capturat----->>>')
  #print(second_value_html)
  print(name.split()[0])
  



  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()


#hola








