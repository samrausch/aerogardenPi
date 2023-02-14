import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)
print(i2c.scan())

