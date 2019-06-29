#Universitat de Barcelona. Domotica
#2019
#Authors:
#         Arnau Vicente Puiggros - GitHub: @arnaudeveloper
#         Alvaro Baucells Costa

import machine
import ssd1306
import utime
import functions
import network
import socket
import struct

#---Variables-----------------------------------------------

host='192.168.4.1'                                          #necesitem ip del NCAP, que al primer socket actua com a servidor (host) 
port=2000                                                   #port del primer socket
s=None
data=''
ssid = 'NCAP'                                               #dades de la xarxa del NCAP
connection = False
password = 'esp32ibz'



i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))   #inicializa I2C
oled = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3c)   #inicializa pantalla
oled.fill(0)          #texto de inicio 

#oled.text(">", 120, 25)
oled.text("Welcome!", 30, 25)  
oled.invert(0)
oled.show()
utime.sleep_ms(800)

devices = i2c.scan()    #escanea dispositivos conectados por i2c
oled.text("Initializing", 15, 40)
oled.text("......", 40, 50)

oled.show()
utime.sleep_ms(3000)
oled.show()
oled.fill(0)
oled.show()

def init_GPIOs():
    global up_pin, down_pin, ok_pin, left_pin, right_pin 
    global irq_up, irq_down, irq_ok, irq_left, irq_right 
    global adc
    
    up_pin = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)   #configuramos los gpios como entradas para el joystick
    down_pin = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
    ok_pin = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
    left_pin = machine.Pin(26, machine.Pin.IN, machine.Pin.PULL_UP)
    right_pin = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)
    
    up_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=irq_up)    #asignamos la interrupcion y la funcion a la que llama
    down_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=irq_down)
    ok_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=irq_ok)
    left_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=irq_left)
    right_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=irq_right)
    
    #adc = machine.ADC(machine.Pin(35))
    #adc.atten(machine.ADC.ATTN_11DB)

def Llegir_adc():
  print("DEBUG=============>")
  adc = machine.ADC(machine.Pin(35))
  adc.atten(machine.ADC.ATTN_11DB)
  
  adc_sum=0
  for x in range(10):
    adc_sum+=adc.read()
    #print(x)
  #exit=0
  adc_sum=adc_sum/10      #mA
  adc_sum = adc_sum/1000  #A
  
  print("RAW: ",str(adc_sum))
  adc_sum = 220*adc_sum   #mW
  print("POT: ",str(adc_sum))
  
  return adc_sum
  

def Llegir_TEDS():
  f=open('Meta_TEDS.dat','rb')
  buffer=f.read()
  f.close()
  print(buffer)
  return buffer
  
  
def Analitzar_comanda(request):
  data=struct.pack('f',1)
  if request==128:
    data=Llegir_adc()
    data=struct.pack('f',data)
    
    comanda="Llegir"
    
  elif request==160:
    data=Llegir_TEDS()
    comanda="Llegir TEDS"
  elif request==3:
    comanda="Definir canal trigger"
  elif request==255:
    comanda="Trigger"
  elif request==0:
    comanda="Escriure"
  else:
    comanda="NO WORK"
    
  return comanda,data
  
init_GPIOs()





  
estados= ['Ninguno', 'ok', 'arriba', 'abajo', 'izquierda', 'derecha']   #variables para elegir el menu con interrupciones
modos = ['Modo_inicial', 'Modo_Automatico', 'Modo_Wifi']

oled.fill(0)
oled.show()
exit=0
state='Ninguno'
state2='Ninguno'
Modo='Modo_inicial'
press=0




while(1):
  if Modo=='Modo_inicial':
    if state is 'Ninguno':
      #oled.fill_rect(121, 50, 128, 8, 0)
      oled.fill_rect(0, 50, 15, 8, 0)
      oled.text('MENU PRINCIPAL', 10, 10)
      oled.hline(0,19, 128, 1)
      oled.show()
      oled.text('MODO AUTOMATICO', 15, 30)
      oled.text(">", 0, 30)
      utime.sleep_ms(90)
      oled.text('MODO WIFI', 15, 50) 
      oled.show()
      #azul(200)
      
    elif state is 'derecha':
      Modo=modos[1]
      oled.fill(0)
      oled.show()
      state='Ninguno'
      exit=0
      
    elif state is 'abajo':
      oled.fill_rect(0, 30, 15, 8, 0)
      oled.show()
      oled.text('MENU PRINCIPAL', 10, 10)
      oled.hline(0,19, 128, 1)
      oled.show()
      oled.text('MODO AUTOMATICO', 15, 30)
      utime.sleep_ms(90)
      oled.text('MODO WIFI', 15, 50) 
      oled.text(">", 0, 50)
      oled.show()
    
      
      if state2 is 'derecha':
        Modo=modos[2]
        oled.fill(0)
        oled.show()
        state2='Ninguno'
        state='Ninguno'
        exit=0
        
      if state is 'arriba':
        Modo=modos[0]
        state='Ninguno'
      else:
        pass
    
    
  elif Modo== 'Modo_Automatico':
    if exit==1:
      #print('DEBUG====> surto del mode AUTOMATICO')

      utime.sleep_ms(100)
      Modo='Modo_inicial'
      state='Ninguno'
      state2='Ninguno'
      exit=0
      oled.fill(0)
      oled.show()
    else:  
      #print('DEBUG=====>',exit)
      oled.text('MODO AUTOMATICO', 5, 10)
      oled.hline(0,19, 128, 1)
      oled.text('<Salir', 0, 55)
      oled.text('Pot (W):', 0, 35)      #muestra el valor por pantalla
      oled.show()
      
      oled.fill_rect(65, 35, 128, 8, 0)

      adc_sum=0
      adc_sum=Llegir_adc()
      '''
      for x in range(10):
        adc_sum+=adc.read()
        #print(x)
      exit=0
      adc_sum=adc_sum/10      #mA
      adc_sum = adc_sum/1000  #A
      
      print("RAW: ",str(adc_sum))
      adc_sum = 220*adc_sum   #mW
      print("POT: ",str(adc_sum))
      '''
      
      #adc_sum = adc_sum/100    #Correction 1
      #adc_sum = adc_sum*6.4    #Correction 1



      #print('DEBUG=====>',exit)
      #print(adc_sum)
      #print('DEBUG=====>',exit)
     
      
      adc_value_to_string= "{:4.1f}".format(adc_sum)
      oled.text(adc_value_to_string, 90, 35)      #muestra el valor por pantalla
      utime.sleep_ms(200)
      #utime.sleep_ms(2000)
      oled.show()
      #print('DEBUG=====>',exit)
      #exit=0

    

      
    
  elif Modo== 'Modo_Wifi':
    exit=0
    oled.text('MODO WIFI', 15, 10)
    oled.hline(0,19, 128, 1)
    oled.text('<Salir', 0, 55)
    oled.show()

    try:
      print("DEBUG===============>1")
      
      while connection == False:
        
        station = network.WLAN(network.STA_IF)          #el TIM el configurem com a estacio, que accedeix a la xarxa del NCAP
        station.active(True) 
        
        functions.Ens_conectem_a_la_red(ssid,password,station)
        
        connection = True 
        print("DEBUG===============>2")
      
      print("DEBUG===============>3")    
      ip=station.ifconfig()[0]                      #agafem la nostra ip per obrir el segon socket (ara com servidor)
      print('ip:', ip)
      
      functions.Enviem_ip_al_NCAP(ip,host,port=2000)

      
      #Configuracio del segon socket com a servidor
      print("DEBUG===============>4")    

      s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Es crea el segon socket (utilitzarem port 2005)
      s2.bind((ip,2005))                                      #Enllecem la nostra ip amb el socket que obrirem per escoltar (Servidor)
      s2.listen(5)                                            #Limit de requests que acceptara
      print("DEBUG===============>5")    


      while True:
        print("DEBUG===============>6")    
    
        conn, addr = s2.accept()         #estableix connexio quan rep un request, i guarda la direccio del client
        print('Got a connection from %s' % str(addr))

        request = conn.recv(1024)        #rep missatge del client, amb un limit de 1024 bytes
        #Rebem la instruccio en bytes unpack    
        #request = str(request)    
        #print('Content = %s' % request)  #Printa tot el que ha capturat
        print("Request: ", request)
        recuperem_variable=struct.unpack('hh',request)    #Perfect
        #recuperem_variable=struct.unpack('h',request)    #Perfect
        print("REcuperem variable: ", recuperem_variable)
        comanda = recuperem_variable[0]
        data_guardar=recuperem_variable[1]
        print(comanda)
        print(data_guardar)

        
        #request=request.split("'")[1]  
        num_de_funcio,data_send=Analitzar_comanda(comanda)
        print("Num de funcio: ",num_de_funcio)
        print("DEBUG===============>7")    
        
        #data_send=struct.pack('f',data)
        
        response = data_send              #missatge que li tornem al client (en funcio del que demani)
        #Enviem la resposta en bytes pack
        conn.sendall(response)           #Enviem la resposta
        
        conn.close()                     #Tanquem connexio per esperar la seguent connexio (es crea a l'inici del while)
        print("DEBUG===============>8")    
        
        oled.fill_rect(0, 30, 128, 8, 0)
        oled.text(str(data_guardar), 60, 30)
        oled.show()
        
        if exit==1:
          break  
      
      #oled.hline(0,19, 128, 1)
      #oled.text('<Salir', 0, 55)
      #oled.text('Lux:', 35, 35)      #muestra el valor por pantalla
      #oled.text('(ok)', 0, 35)
      #oled.show()
      

        
    except:
     if (s2):    
      s2.close()                       #si esta obert el socket, el tanca per evitar problemes a l'hora de tornar-lo a obrir en un futur
    s2.close()
    station.disconnect()               #si s'ha parat el programa, es desconecta de la xarxa
    station.active(False)
  
     
    #if exit==1:
    utime.sleep_ms(100)
    Modo='Modo_inicial'
    state='abajo'
    state2='Ninguno'
    oled.fill(0)
    oled.show()
      
      
  else:
    pass
  
  
