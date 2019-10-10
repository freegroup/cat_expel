"""
#Installing v4l-utils (debian) gives one the handy v4l2-ctl command:
$ v4l2-ctl --list-devices
HPigh Definition Webcam (usb-0000:00:14.0-11):
    /dev/video2
UVC Camera (046d:0821) (usb-0000:00:14.0-13):
    /dev/video0
Logitech Webcam C930e (usb-0000:00:14.0-9):
    /dev/video1
. . . which can be accessed thusly:
"""
from  subprocess import Popen, PIPE

def find_cam(cam):
    cmd = ["/usr/bin/v4l2-ctl", "--list-devices"]
    out, err = Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()
    out, err = out.strip(), err.strip()
    out = out.decode()
    for l in [i.split("\n\t") for i in out.split("\n\n")]:
        if cam in l[0]:
            return l[1]
    return False
    
if __name__ == "__main__":
    cam="UVC"
    print(find_cam(cam))