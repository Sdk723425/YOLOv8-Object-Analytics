class RegionCounter:
    def __init__(self, zones):
        self.zones = zones
        self.counts = {zone: set() for zone in zones}

    def update(self, frame, results):
        annotated = frame.copy()
        object_data = []
        if results[0].boxes.id is not None:
            for box, obj_id in zip(results[0].boxes.xyxy, results[0].boxes.id):
                x1, y1, x2, y2 = box
                cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
                for zone_name, polygon in self.zones.items():
                    if cv2.pointPolygonTest(np.array(polygon, np.int32), (cx, cy), False) >= 0:
                        self.counts[zone_name].add(int(obj_id))
                object_data.append({'id': int(obj_id), 'center': (cx, cy)})
        return annotated, object_data
