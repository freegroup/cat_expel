from hal.raspi.motor import Motor
import hal.raspi.camera as camera

class Hardware:

    Camera = camera.Camera()

    Motor1 = Motor(1)
    Motor2 = Motor(2)
    Motor3 = Motor(3)

