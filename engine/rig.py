from engine.actions import get_action_frame


class CharacterRig:
    def __init__(self, name="main_character"):
        self.name = name
        self.x = 0
        self.y = 0
        self.action = "idle"
        self.scale = 1.0
        self.facing = 1

    def play(self, action):
        self.action = action

    def update(self, time_seconds):
        frame = get_action_frame(
            self.action,
            time_seconds
        )

        return {
            "name": self.name,
            "x": self.x + frame["x"],
            "y": self.y + frame["y"],
            "pose": frame["pose"],
            "scale": self.scale,
            "facing": self.facing,
        }

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def set_scale(self, scale):
        self.scale = max(0.1, scale)

    def turn(self, direction):
        self.facing = -1 if direction == "left" else 1
      
