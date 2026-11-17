class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.zoom = 1.0
        self.target_x = 0
        self.target_y = 0

    def follow(self, x, y):
        self.target_x = x
        self.target_y = y

    def update(self, smoothness=0.08):
        self.x += (self.target_x - self.x) * smoothness
        self.y += (self.target_y - self.y) * smoothness

    def set_zoom(self, zoom):
        self.zoom = max(0.2, min(zoom, 3.0))

    def get_position(self):
        return {
            "x": self.x,
            "y": self.y,
            "zoom": self.zoom,
        }
      
