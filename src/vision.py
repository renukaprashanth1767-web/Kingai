import cv2
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

class EVVision:
    """
    E.V. Vision Module
    Handles webcam feeds and uses OpenCV for tracking living things (faces/bodies).
    """
    def __init__(self, camera_index: int = 0):
        self.camera_index = camera_index
        # Load pre-trained Haar Cascades for face and full body detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
        self.cap = None

    def start_camera(self) -> bool:
        """Initializes the camera capture."""
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            logger.error(f"Failed to open camera at index {self.camera_index}")
            return False
        logger.info("Camera started successfully.")
        return True

    def stop_camera(self) -> None:
        """Releases the camera and closes windows."""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        logger.info("Camera stopped.")

    def process_frame(self, frame) -> Tuple[object, int]:
        """
        Processes a single frame, detecting living things (faces/bodies),
        drawing HUD bounding boxes, and returning the annotated frame
        along with the count of detected entities.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        # Detect bodies
        bodies = self.body_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(50, 50))

        entity_count = len(faces) + len(bodies)

        # Draw HUD for faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, "TARGET: FACE", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Draw HUD for bodies
        for (x, y, w, h) in bodies:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 165, 255), 2)
            cv2.putText(frame, "TARGET: BODY", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 2)

        # Draw general HUD telemetry
        cv2.putText(frame, "E.V. TACTICAL HUD ONLINE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        cv2.putText(frame, f"ENTITIES TRACKED: {entity_count}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        return frame, entity_count

    def run_tracking_loop(self) -> None:
        """
        Runs the main video loop. Press 'q' to exit.
        """
        if not self.start_camera():
            return

        print("Starting E.V. Vision Tracking... Press 'q' to quit.")

        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    logger.error("Failed to read frame from camera.")
                    break

                annotated_frame, count = self.process_frame(frame)

                cv2.imshow('E.V. Vision System', annotated_frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            self.stop_camera()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    vision = EVVision()
    vision.run_tracking_loop()
