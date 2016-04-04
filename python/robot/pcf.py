import wiringpi

pin_base = 65
i2c_addr = 0x21
pins = [65,66,67,68,69,70,71,72]

wiringpi.wiringPiSetup()
wiringpi.pcf8474Setup(pin_base,i2c_addr)

for pin in pins:
	wiringpi.pinMode(pin,1)
	wiringpi.digitalWrite(pin,1)
	wiringpi.delay(1000)
	wiringpi.digitalWrite(pin,0)
