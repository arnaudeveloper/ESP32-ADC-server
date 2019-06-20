import network
import machine
import socket
import utime


host2='192.168.4.2'
#port=2000
p2=2001
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
 
 
Configuracio_acces_point(essid,password)

#c=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

 

#try:
  
ip=ap.ifconfig()[0]                                 #get ip addr
port=2000

#Configuracio_del_socket_server(ip,port)  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                   #create socket
s.bind((ip,port))                                                       #Enllecem la ip amb el  port
s.listen(5)                                                             #listen message

count=0  

while count<1:
  
  conn, addr = s.accept()                                   #Crea una connexio quan el client envia un request
  print('Got a connection from %s' % str(addr))
  
  request = conn.recv(1024)                                 #Capturem el missatge del client
  request = str(request)                                    #Ho convertim a string
  print('Content = %s' % request)                           #Printem el missatge
  
  utime.sleep_ms(500)
  
  ip_TIM=request.split("'")[1]                              #Separem la IP
  print('ip del tim:', ip_TIM)
  
  response = ip_TIM + '+ ok'                                #Creem la reposta
  conn.sendall(response)                                    #Enviem la resposta
  
  conn.close()                                              #Tanquem la connexio 
  
  count=count+1                                             #Contador de ESP connectats
  print('count',count)
  
  if count==1:                                              #Si hem arribat al limit tanquem el socket
    s.close()      
print('iniciem config client')

print('DEBUG===================>>')

#----------------Fins aqui OK
#Configuracio com a client

#Inciem un socket client per demanar info al TIM
addr_info = socket.getaddrinfo("towel.blinkenlights.nl", 23)          #MAGIC!
print(addr_info)

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.close()

utime.sleep_ms(5000)


print('DEBUG===================>>')
p2=2005
ip_TIM='192.168.4.2'


while True:
  s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  #c.connect((host2, p2))
  #c.connect((192.168.4.2, p2))
  
  #s.connect(('192.168.4.2', p2))                        #Ens connectem al socket
  s.connect((ip_TIM, p2))                                 #Ens connectem al socket
  print('DEBUG===================>>')

  
  msg='hola servidor'
  s.send(msg)
  print('DEBUG===================>>')

  data=s.recv(1024)
  print(data)
  s.close()
  utime.sleep_ms(5000)
    



 

