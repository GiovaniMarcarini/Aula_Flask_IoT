import Adafruit_DHT as dht
import RPi.GPIO as gpio
import time as delay
from app import app
from flask import render_template


gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)

ledvermelho = 11
ledverde = 12
pin_dht = 4
pin_t = 15 
pin_e = 16
lixeira_v = 20

dht_sensor = dht.DHT11

stsledred = ''
stsledgreen = ''

gpio.setup(ledvermelho, gpio.OUT)
gpio.setup(ledverde, gpio.OUT)
gpio.setup(pin_t, gpio.OUT)
gpio.setup(pin_e, gpio.IN)

gpio.output(ledvermelho, gpio.LOW)
gpio.output(ledverde, gpio.LOW)

def statusledvermelho():
    if gpio.input(ledvermelho) == 1:
        statusledvermelho = 'LED vermelho ON'
    else:
        statusledvermelho = 'LED vermelho OFF' 
    return statusledvermelho

def statusledverde():
    if gpio.input(ledverde) == 1:
        statusledverde = 'LED verde ON'
    else:
        statusledverde = 'LED verde OFF'
    return statusledverde

def umid_temp():
    umid, temp = dht.read(dht_sensor, pin_dht)
    if umid is not None:
        umidade = ('{0:0.0f}%'.format(umid))
    else:
        umidade = 'Erro ao ler sensor'
    if temp is not None:
        temperatura = ('{0:0.0f}*C'.format(temp, umid))
    else:
        temperatura = 'Erro ao ler sensor'
    return umidade, temperatura

def ocupacao_lixeira():
    gpio.output(pin_t, True)
    delay.sleep(0.000001)
    gpio.output(pin_t, False)
    tempo_i = delay.time()
    tempo_f = delay.time()
    
    while gpio.input(pin_e) == False:
        tempo_i = delay.time()
    while gpio.input(pin_e)  == True:
        tempo_f = delay.time()
     
    tempo_d = tempo_f - tempo_i
    
    distancia = (tempo_d*34300)/2

    ocupacao_l = (distancia/lixeira_v)*100
    ocupacao_f = 100 - ocupacao_l
    ocupacao_lixeira = ('{0:0.0f}%'.format(ocupacao_f))
    return ocupacao_lixeira

@app.route("/")
def index():
    templateData = {
        'ledred'  : statusledvermelho(),
        'ledgreen' : statusledverde(),
        'umid' : umid_temp()[0],
        'temp' : umid_temp()[1],
        'ocup_lixeira' :  ocupacao_lixeira(),
    }
    return render_template('index.html', **templateData)

@app.route("/led_vermelho/<action>")
def led_vermelho(action):
    if action == 'on':
        gpio.output(ledvermelho, gpio.HIGH)
    if action == 'off':
        gpio.output(ledvermelho, gpio.LOW)

    templateData = {
        'ledred'  : statusledvermelho(),
        'ledgreen' : statusledverde(),
        'umid' : umid_temp()[0],
        'temp' : umid_temp()[1],
        'ocup_lixeira' :  ocupacao_lixeira(),
    }
    return render_template('index.html', **templateData)

@app.route("/led_verde/<action>")
def led_verde(action):
    if action == 'on':
        gpio.output(ledverde, gpio.HIGH)
    if action == 'off':
        gpio.output(ledverde, gpio.LOW)
        
    templateData = {
        'ledred'  : statusledvermelho(),
        'ledgreen' : statusledverde(),
        'umid' : umid_temp()[0],
        'temp' : umid_temp()[1],
        'ocup_lixeira' :  ocupacao_lixeira(),
    }
    return render_template('index.html', **templateData)