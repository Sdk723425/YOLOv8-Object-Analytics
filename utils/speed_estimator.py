import time
import numpy as np

class SpeedEstimator:
    def __init__(self):
        self.last_positions = {}
        self.last_time = time.time()

    def update(self, objects):
        current_time = time.time()
        dt = current_time - self.last_time
        for obj in objects:
            obj_id = obj['id']
            cx, cy = obj['center']
            if obj_id in self.last_positions:
                dx = cx - self.last_positions[obj_id][0]
                dy = cy - self.last_positions[obj_id][1]
                dist = np.sqrt(dx**2 + dy**2)
                speed = dist / dt
                print(f"Object {obj_id} speed: {speed:.2f} px/s")
            self.last_positions[obj_id] = (cx, cy)
        self.last_time = current_time
