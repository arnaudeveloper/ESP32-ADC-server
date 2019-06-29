


import machine
import ssd1306
import utime
import functions
import network



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
    
    adc = machine.ADC(machine.Pin(35))
    adc.atten(machine.ADC.ATTN_11DB)

    
init_GPIOs()





  
estados= ['Ninguno', 'ok', 'arriba', 'abajo', 'izquierda', 'derecha']   #variables para elegir el menu con interrupciones
modos = ['Modo_inicial', 'Modo_Automatico', 'Modo_Manual']

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
      oled.text('Opcio 2', 15, 50) 
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
      oled.text('Opcio 2', 15, 50) 
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
      for x in range(10):
        adc_sum+=adc.read()
        #print(x)
      exit=0
      adc_sum=adc_sum/10      #mA
      adc_sum = adc_sum/1000  #A
      
      print("RAW: ",str(adc_sum))
      adc_sum = 220*adc_sum   #mW
      print("POT: ",str(adc_sum))
      
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

    

      
    
  elif Modo== 'Modo_Manual':
    oled.text('MODO MANUAL', 15, 10)
    oled.hline(0,19, 128, 1)
    oled.text('<Salir', 0, 55)
    oled.text('Lux:', 35, 35)      #muestra el valor por pantalla
    oled.text('(ok)', 0, 35)
    oled.show()
    
        
    if press is 1:
      oled.fill_rect(0, 35, 32, 10, 0)        
      oled.show()
      utime.sleep_ms(2000)
      oled.fill_rect(70, 35, 128, 8, 0)       #borra el valor dos segundos despues de mantenerlo en pantalla
      oled.show()
      press=0
    oled.text('(ok)', 0, 35)
      
    if exit==1:
      utime.sleep_ms(100)
      Modo='Modo_inicial'
      state='abajo'
      state2='Ninguno'
      oled.fill(0)
      oled.show()
      
      
  else:
    pass
  
 
