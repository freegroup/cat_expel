
def write_history(context):
    last_frames = context.last_frames
    image = context.current_frame

    last_frames.put(image)
    if last_frames.qsize() > 60:
        last_frames.get()
