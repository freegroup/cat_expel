import threading

class ImageCache:

    def __init__(self, max_size=20):
        self.lock = threading.RLock()
        self.stack = []
        self.max_size = max_size

    def forwarding_image(self):
        return self.peek()

    def debug_image(self):
        return self.peek()

    def push(self, image):
        try:
            self.lock.acquire()
            self.stack.append(image)
            if len(self.stack) > self.max_size:
                self.stack.pop(0)
        finally:
            self.lock.release()

        print(len(self.stack))

    def pop(self):
        try:
            self.lock.acquire()
            if len(self.stack) < 1:
                return None
            return self.stack.pop(0)
        finally:
            self.lock.release()

    def peek(self):
        try:
            self.lock.acquire()
            if len(self.stack) < 1:
                return None
            return self.stack[-1]
        finally:
            self.lock.release()
