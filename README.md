# cat_expel

udevadm info --name=/dev/video0 --attribute-walk
udevadm info --name=/dev/video0 --attribute-walk
udevadm info --name=/dev/video0 --attribute-walk

sudo vi /etc/udev/rules.d/10-usb-video.rules
sudo udevadm trigger

ls -la /dev/v*udevadm info --name=/dev/video0 --attribute-walk
sudo udevadm trigger

 udevadm info -a -p  $(udevadm info -q path -n /dev/video1)


```
docker buildx build --platform linux/arm64 -t cat_expel:0.1 .
```
