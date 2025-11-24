import machine
import time

# Nastavení UART0: Rychlost 115200 (musí být stejná na RPi 4), TX=GP0, RX=GP1
uart = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1))

print("UART připraven. Čekám na data z RPi 4...")

while True:
    if uart.any():  # Pokud jsou v zásobníku nějaká data
        data = uart.read()  # Přečti všechna dostupná data
        
        # Pokus o dekódování pro hezčí výpis (volitelné)
        try:
            print(f"Přijato: {data.decode('utf-8')}")
        except:
            print(f"Přijato (raw): {data}")
            
    time.sleep(0.05) # Krátká pauza pro ulehčení procesoru