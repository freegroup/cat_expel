from hal import Hardware

def source_get_images():
    while True:
        try:
            yield Hardware.Camera.read()
        except:
            print("error....")
