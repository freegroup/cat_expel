import time
from motor import Motor
from switch import Switch

motor1 = Motor([23,24,25,4])
motor2 = Motor([17,18,27,22])
end = Switch(15)


while True:
    if not end.pressed():
        motor1.step(1)
        motor2.step(1)
        time.sleep(0.004)
