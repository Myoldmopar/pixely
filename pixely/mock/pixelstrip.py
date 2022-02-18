class MockStrip:

    def __init__(self):
        self.response = None

    def set_next_response(self, x):
        self.response = x

    def clear_response(self):
        self.response = None

    def setPixelColor(self, x, color):
        return self.response

    def show(self):
        return self.response
