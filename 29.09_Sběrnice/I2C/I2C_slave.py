# i2c_slave_lib.py
import time
 
class I2CSlave:
    """
    Simulovaný I2C slave pro testování master zařízení.
    Nativní I2C slave na CircuitPython/Pico není podporováno,
    takže toto je pro software simulaci.
    """
 
    def __init__(self, address=0x42, buffer_size=32):
        self.address = address
        self.buffer_size = buffer_size
        self._buffer = bytearray(buffer_size)
        self._has_new_data = False
 
    def receive(self, data: bytes):
        """
        Simulace příjmu dat od mastera.
        Ukládá je do bufferu.
        """
        length = min(len(data), self.buffer_size)
        self._buffer[:length] = data[:length]
        self._has_new_data = True
        print(f"[DEBUG] Data received at 0x{self.address:X}: {data}")
 
    def read(self):
        """
        Vrátí data z bufferu, pokud jsou nová.
        """
        if self._has_new_data:
            self._has_new_data = False
            return self._buffer.rstrip(b'\x00')
        return None
 
    def has_data(self):
        return self._has_new_data
 
 
# --- Example usage ---
if __name__ == "__main__":
    slave = I2CSlave(address=0x42)
 
    print("Simulated I2C Slave Ready at address 0x42")
 
    while True:
        # simulace master posílá '1' každou sekundu
        slave.receive(b'1')
 
        received = slave.read()
        if received:
            print("Received:", received)
        time.sleep(1)