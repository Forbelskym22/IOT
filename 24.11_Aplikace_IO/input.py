from machine import Pin
import time


class Tlacitko:
    def __init__(self, pin, debounce_ms=50):
        self.pin = pin
        self.debounce_ms = debounce_ms
        self.posledni_cas_stisku = 0
        self.posledni_stav = 1
        

        self.pin.init(Pin.IN, Pin.PULL_UP)

    def bylo_stisknuto(self):
        aktualni_stav = self.pin.value()
        aktualni_cas = time.ticks_ms()
        vysledek = False

        if aktualni_stav == 0 and self.posledni_stav == 1:
            if time.ticks_diff(aktualni_cas, self.posledni_cas_stisku) > self.debounce_ms:
                self.posledni_cas_stisku = aktualni_cas
                vysledek = True 
                
        if aktualni_stav == 1:
            self.posledni_stav = 1
        elif vysledek:
            self.posledni_stav = 0

        return vysledek

    def je_drzeno(self):

        return self.pin.value() == 0