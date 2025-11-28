# Simple test class used for testing steering
import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)
mp_draw = mp.solutions.drawing_utils


def compute_angle(left, right):
    dx = right.x - left.x
    dy = right.y - left.y
    angle = math.degrees(math.atan2(dy, dx))
    return angle


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    steering_state = "no hands detected"

    if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 2:

        hand1, hand2 = results.multi_hand_landmarks

        # Sort hands by x-position (left vs right)
        if hand1.landmark[0].x < hand2.landmark[0].x:
            left_hand = hand1
            right_hand = hand2
        else:
            left_hand = hand2
            right_hand = hand1

        lw = left_hand.landmark[0]
        rw = right_hand.landmark[0]

        # Draw hand landmarks
        mp_draw.draw_landmarks(frame, left_hand, mp_hands.HAND_CONNECTIONS)
        mp_draw.draw_landmarks(frame, right_hand, mp_hands.HAND_CONNECTIONS)

        # Compute steering wheel angle
        angle = compute_angle(lw, rw)

        # Normalize angle (-90 to 90)
        if angle > 90:
            angle -= 180
        if angle < -90:
            angle += 180

        # Determine steering state
        if abs(angle) < 15:
            steering_state = "straight"
        elif angle > 15:
            steering_state = "right"
        elif angle < -15:
            steering_state = "left"

        # Display angle
        cv2.putText(frame, f"Angle: {int(angle)} deg", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    else:
        cv2.putText(frame, "Show BOTH hands!", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Print steering state in console
    print("Steering:", steering_state)

    cv2.putText(frame, f"State: {steering_state}", (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow("Steering Test", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
