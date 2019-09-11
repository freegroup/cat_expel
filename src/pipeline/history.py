from file.configuration import Configuration

conf = Configuration(inifile="config/service.ini", reload_on_change=True)

def write_history(context):
    last_frames = context.last_frames
    image = context.current_frame

    last_frames.put(image)
    if last_frames.qsize() > conf.get_int("frames", section="history"):
        last_frames.get()
