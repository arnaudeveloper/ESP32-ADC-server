
## boot.py
## developerarnau@gmail.com
## GitHub: @arnaudeveloper

from machine import Pin,I2C,ADC
from time import sleep

import ssd1306
import network                            ##Llibreria
import gc
gc.collect()

i2c = I2C(-1,scl=Pin(22), sda=Pin(21))
devices=i2c.scan()
#print(devices) #debug

lcd = ssd1306.SSD1306_I2C(128,64,i2c) 
lcd.fill(0)

lcd.text("Initializing",0,0)
lcd.show()

sleep(1)
  
station = network.WLAN(network.STA_IF)    ##Creem una estacio, dispositiu que es pot connectar a una red
station.active(True)                      ##Activem l'estacio

station.connect("death-note", "C@BRONES!miWIFI!") ##Usuari i contrasenya de la red
for x in range(128):
  lcd.text(".",x,8)
  lcd.show()

while station.isconnected() == False:
  pass
  
station.ifconfig()                        ## Ens retorna la configuracio de la connexio
ip=station.ifconfig()[0]
print('Connection successful')
print(station.ifconfig())
print('Connected to:',ip)
lcd.text("Connection",0,24)
lcd.text("Succesful",0,32)
lcd.text(ip,0,40)

lcd.show()
sleep(2)



print('end wifi')



