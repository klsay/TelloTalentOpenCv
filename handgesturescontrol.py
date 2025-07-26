import cv2
import mediapipe as mp
import time
from djitellopy import tello


# Connect to the drone (adjust for your connection)
#droneObject = tello.Tello()
#droneObject.connect()


# MediaPipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands = 1, 
                       min_detection_confidence = 0.7)

def detect_gesture(landmarks, wrist_y, wrist_x):
    tips = [landmarks[mp_hands.HandLandmark.THUMB_TIP],
            landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP],
            landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
            landmarks[mp_hands.HandLandmark.RING_FINGER_TIP],
            landmarks[mp_hands.HandLandmark.PINKY_TIP]]
    
    if (all(tip.y < wrist_y for tip in tips) and 
        landmarks[mp_hands.HandLandmark.THUMB_TIP].x < landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x):
        return "Takeoff"
    elif all(tip.y > wrist_y for tip in tips):
        return "Land"

    
    elif (landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x < wrist_x and
          landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x < landmarks[mp_hands.HandLandmark.THUMB_TIP].x and  
          landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x < landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x and 
          landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x < landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].x and 
          landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x < landmarks[mp_hands.HandLandmark.PINKY_TIP].x and
          landmarks[mp_hands.HandLandmark.INDEX_FINGER_MCP].y < landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y and
          landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y < landmarks[mp_hands.HandLandmark.RING_FINGER_MCP].y and
          landmarks[mp_hands.HandLandmark.RING_FINGER_MCP].y < landmarks[mp_hands.HandLandmark.PINKY_MCP].y):
        
        return "Roll Left"
        
    
    
    elif (landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x > wrist_x and 
          landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x > landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x and 
          landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x > landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].x and 
          landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x > landmarks[mp_hands.HandLandmark.PINKY_TIP].x):
        return "Roll Right"
    

    elif (landmarks[mp_hands.HandLandmark.PINKY_TIP].x < wrist_x and 
          landmarks[mp_hands.HandLandmark.PINKY_TIP].x < landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x and 
          landmarks[mp_hands.HandLandmark.PINKY_TIP].x < landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].x and 
          landmarks[mp_hands.HandLandmark.PINKY_TIP].x < landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x and
          landmarks[mp_hands.HandLandmark.INDEX_FINGER_MCP].y < landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y and
          landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y < landmarks[mp_hands.HandLandmark.RING_FINGER_MCP].y and
          landmarks[mp_hands.HandLandmark.RING_FINGER_MCP].y < landmarks[mp_hands.HandLandmark.PINKY_MCP].y):
        return "Yaw Left"
    
    elif (landmarks[mp_hands.HandLandmark.PINKY_TIP].x > wrist_x and 
          landmarks[mp_hands.HandLandmark.PINKY_TIP].x > landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x and 
          landmarks[mp_hands.HandLandmark.PINKY_TIP].x > landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].x and 
          landmarks[mp_hands.HandLandmark.PINKY_TIP].x > landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x and
          landmarks[mp_hands.HandLandmark.INDEX_FINGER_MCP].y < landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y and
          landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y < landmarks[mp_hands.HandLandmark.RING_FINGER_MCP].y and
          landmarks[mp_hands.HandLandmark.RING_FINGER_MCP].y < landmarks[mp_hands.HandLandmark.PINKY_MCP].y):
        return "Yaw Right"

    
    elif (landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < wrist_y and
          landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < landmarks[mp_hands.HandLandmark.INDEX_FINGER_DIP].y and
          landmarks[mp_hands.HandLandmark.THUMB_TIP].x > landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x):
        return "Pitch Forward"
    
    elif (landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < wrist_y and
          landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y > landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP].y and
          landmarks[mp_hands.HandLandmark.THUMB_TIP].x > landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x):
        return "Pitch Backward"
    else:
        return "Idle"

def send_movement(command):
    if command == "Takeoff":
        print("Taking off...")
        time.sleep(2)
    elif command == "Land":
        print("Landing...")
    elif command == "Roll Left":
        print("Rolling left")
    elif command == "Roll Right":
        print("Rolling right")
    elif command == "Pitch Forward":
        print("Pitching forward")
    elif command == "Pitch Backward":
        print("Pitching backward")
    else:
        return "Idle"

# Camera stream
cap = cv2.VideoCapture(0)
prev_command = ""

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
            wrist = hand.landmark[mp_hands.HandLandmark.WRIST]
            gesture = detect_gesture(hand.landmark, wrist.y, wrist.x)

            if gesture != prev_command:
                send_movement(gesture)
                prev_command = gesture

            cv2.putText(frame, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('Drone Control', frame)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
