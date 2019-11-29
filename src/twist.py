from motor import Motor
from switch import Switch

motor = Motor([23,24,25,4])
end = Switch(15)


while True:
    if not end.pressed():
        motor.step(1)
