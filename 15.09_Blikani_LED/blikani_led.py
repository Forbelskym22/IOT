from machine import Pin
import time

# Inicializace pinu – například GPIO 15
led = Pin("LED", Pin.OUT)

def zapnout_led():
    #Zapne LED pomocí .value()
    led.value(1)
    print("LED zapnuta")

def vypnout_led():
    #Vypne LED pomocí .value()
    led.value(0)
    print("LED vypnuta")

def prepni_led():
    #zneguje stav pinu
    led.toggle()
    print("LED přepnuta (toggle)")

def precti_stav():
    #Vrátí aktuální stav LED (0 nebo 1)
    stav = led.value()
    print("Aktuální stav LED:", stav)
    return stav


# Hlavní smyčka – ukázka
def hlavni():
    while True:
        zapnout_led()
        time.sleep(1)

        vypnout_led()
        time.sleep(1)

        prepni_led()
        time.sleep(1)

        precti_stav()
        time.sleep(1)

# Spuštění hlavní smyčky
hlavni()
