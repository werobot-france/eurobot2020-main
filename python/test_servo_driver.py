from time import sleep
from src.PWMDriver import PWMDriver

driver = PWMDriver()
driver.setAngle(0, 180)
sleep(1.5)
driver.setAngle(0, 0)
