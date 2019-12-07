from hal import Hardware

def source_get_images():
    while True:
        yield Hardware.Camera.read()
