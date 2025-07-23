import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.5)

# Open webcam
cap = cv2.VideoCapture(0)

def is_thumb_up(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    # Thumb up condition: thumb above wrist and other fingers folded
    if (thumb_tip.y < thumb_ip.y and
        index_tip.y > thumb_tip.y and
        middle_tip.y > thumb_tip.y and
        ring_tip.y > thumb_tip.y and
        pinky_tip.y > thumb_tip.y):
        return True
    return False

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Flip image for a selfie-view display
    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            if is_thumb_up(hand_landmarks):
                print("thumb up")
                cv2.putText(image, "Thumb Up!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

    cv2.imshow('Thumbs Up Detection', image)
    if cv2.waitKey(5) & 0xFF == 27:  # Press Esc to exit
        break

cap.release()
cv2.destroyAllWindows()