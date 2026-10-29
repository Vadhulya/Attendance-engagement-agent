import time
from collections import defaultdict

class EngagementFusion:
    def __init__(self, sustained_seconds_threshold=5):
        self.threshold = sustained_seconds_threshold
        self.first_seen = {}
        self.confirmed_attendance = set()
        self.engagement_history = []

    def update(self, detected_names, audio_rms):
        now = time.time()

        for name in detected_names:
            if name == "Unknown":
                continue
            if name not in self.first_seen:
                self.first_seen[name] = now
            elif (now - self.first_seen[name]) >= self.threshold:
                self.confirmed_attendance.add(name)

        # Baseline score: Face presence vs noise balance
        face_count = len(detected_names)
        # Moderate RMS indicates active questions/discussion; flatline indicates disengagement or passive silence
        audio_score = min(audio_rms / 800.0, 1.0)
        engagement_metric = 0.6 * (1.0 if face_count > 0 else 0.0) + 0.4 * audio_score

        record = {
            "timestamp": time.strftime("%H:%M:%S"),
            "active_faces": face_count,
            "audio_rms": round(audio_rms, 2),
            "engagement_score": round(min(engagement_metric * 100, 100), 1)
        }
        self.engagement_history.append(record)
        return record