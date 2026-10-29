import os
import cv2
import numpy as np

class VisionTracker:
    def __init__(self, known_faces_dir="data/known_faces"):
        # Load Haar Cascade detector (built directly into OpenCV)
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        # OpenCV LBPH face recognizer
        self.recognizer = cv2.face.LBPHFaceRecognizer_create() if hasattr(cv2, 'face') else None
        self.label_map = {}
        self.known_faces_dir = known_faces_dir
        self.trained = False
        self._load_and_train()

    def _load_and_train(self):
        if not os.path.exists(self.known_faces_dir):
            os.makedirs(self.known_faces_dir, exist_ok=True)
            return

        faces = []
        labels = []
        current_id = 1

        for filename in os.listdir(self.known_faces_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                name = os.path.splitext(filename)[0]
                filepath = os.path.join(self.known_faces_dir, filename)
                img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    continue

                detected = self.face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=4)
                for (x, y, w, h) in detected:
                    face_roi = cv2.resize(img[y:y+h, x:x+w], (100, 100))
                    faces.append(face_roi)
                    labels.append(current_id)
                    self.label_map[current_id] = name
                    current_id += 1

        if faces and self.recognizer:
            self.recognizer.train(faces, np.array(labels))
            self.trained = True

    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detected_faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.2, minNeighbors=5, minSize=(40, 40)
        )

        detected_names = []
        for (x, y, w, h) in detected_faces:
            name = "Student"
            if self.trained and self.recognizer:
                face_roi = cv2.resize(gray[y:y+h, x:x+w], (100, 100))
                label_id, confidence = self.recognizer.predict(face_roi)
                # Lower confidence score in LBPH means closer match
                if confidence < 75 and label_id in self.label_map:
                    name = self.label_map[label_id]
                else:
                    name = "Unregistered"
            detected_names.append(name)

        return {
            "num_faces": len(detected_faces),
            "detected_names": detected_names,
            "boxes": detected_faces
        }