from hal import Hardware

def get_image():
    while True:
        try:
            yield Hardware.Camera.read()
        except:
            print("error....")
