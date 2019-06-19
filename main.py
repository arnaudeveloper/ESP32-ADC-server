


from machine import Pin,I2C,ADC
from time import sleep

import ssd1306


motion = False
def handle_interrupt(pin):
  global motion
  motion = True
  global interrupt_pin
  interrupt_pin = pin 
  
pir_0 = Pin(12, Pin.IN,Pin.PULL_UP) #Configuracio del pin
pir_1 = Pin(13, Pin.IN,Pin.PULL_UP) #Configuracio del pin
pir_2 = Pin(14, Pin.IN,Pin.PULL_UP)
pir_3 = Pin(27, Pin.IN,Pin.PULL_UP)
pir_4 = Pin(26, Pin.IN,Pin.PULL_UP)

pir_0.irq(trigger=Pin.IRQ_FALLING, handler=handle_interrupt)
pir_1.irq(trigger=Pin.IRQ_FALLING, handler=handle_interrupt)
pir_2.irq(trigger=Pin.IRQ_FALLING, handler=handle_interrupt)
pir_3.irq(trigger=Pin.IRQ_FALLING, handler=handle_interrupt)
pir_4.irq(trigger=Pin.IRQ_FALLING, handler=handle_interrupt)

#create ADC object
adc0=ADC(Pin(32)) #SIGNAL+2.5
adc1=ADC(Pin(34))
adc2=ADC(Pin(35))               

i2c = I2C(-1,scl=Pin(22), sda=Pin(21))
devices=i2c.scan()
print(devices)
lcd = ssd1306.SSD1306_I2C(128,64,i2c) 
lcd.fill(0)
lcd.text("ArnauDeveloper",0,0)
lcd.text("lcd.py",0,8)
lcd.text("ADC values:",0,24)
lcd.show() 
print('Config end')

while True:
  if motion:
    print('Motion detected! Interrupt caused by:', interrupt_pin)
    sleep(1)
    print('Motion stopped!')
    motion = False
    
  lcd.fill(0)
  lcd.text("ArnauDeveloper",0,0)
  lcd.text("lcd.py",0,8)
  lcd.text("ADC values:",0,24)
  
  lcd.text("Signal:",0,32)
  lcd.text("Output:",0,40)
  lcd.text("RMS:",0,48)



  lcd.text(str(adc0.read()),80,32)
  lcd.text(str(adc1.read()),80,40)
  lcd.text(str(adc2.read()),80,48)
  lcd.show()
  
  sleep(0.1)





