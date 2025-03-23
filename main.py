import cv2
import mediapipe as mp
import time
from pynput.keyboard import Key, Controller

# Inisialisasi Mediapipe Hand
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# Inisialisasi keyboard controller
keyboard = Controller()

# Inisialisasi webcam
cap = cv2.VideoCapture(0)

# Variabel untuk melacak status gesture
last_gesture = None
gesture_cooldown = 0
cooldown_time = 0.3  # seconds

def count_raised_fingers(hand_landmarks):
    # Mengambil koordinat landmark jari
    fingertips = [
        hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP],        # Ibu jari
        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP], # Telunjuk
        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP], # Jari tengah
        hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],  # Jari manis
        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]         # Kelingking
    ]
    
    finger_mcp = [
        hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP],
        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP],
        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP],
        hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP],
        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]
    ]
    
    finger_pip = [
        None,  # Thumb doesn't have PIP
        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP],
        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP],
        hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP],
        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]
    ]
    
    # Menghitung jari yang terangkat
    raised = [False, False, False, False, False]
    
    # Ibu jari dianggap terangkat jika tip lebih ke kanan/kiri dari MCP (tergantung tangan)
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]
    
    # Deteksi tangan kanan atau kiri
    is_right_hand = thumb_mcp.x < wrist.x
    
    # Untuk ibu jari
    if is_right_hand:
        raised[0] = fingertips[0].x < thumb_mcp.x
    else:
        raised[0] = fingertips[0].x > thumb_mcp.x
    
    # Untuk jari lainnya (dianggap terangkat jika ujung jari di atas PIP)
    for i in range(1, 5):
        if finger_pip[i] is not None:
            raised[i] = fingertips[i].y < finger_pip[i].y
    
    return raised

def detect_gesture(hand_landmarks):
    raised = count_raised_fingers(hand_landmarks)
    
    # Gesture 1 (Angka 1): Hanya telunjuk terangkat, arrow key kiri
    if not raised[0] and raised[1] and not raised[2] and not raised[3] and not raised[4]:
        return "KIRI"
    
    # Gesture 2 (Angka 2): Telunjuk dan jari tengah terangkat, arrow key kanan
    elif not raised[0] and raised[1] and raised[2] and not raised[3] and not raised[4]:
        return "KANAN"
    
    # Gesture mengepal: Semua jari tidak terangkat, arrow key bawah
    elif not any(raised):
        return "TURUN"
    
    # Gesture membuka: Semua jari terangkat, arrow key atas
    elif all(raised[1:]):  # Kecuali ibu jari
        return "LOMPAT"
    
    return None

def press_key(gesture):
    if gesture == "KIRI":
        keyboard.press(Key.left)
        keyboard.release(Key.left)
    elif gesture == "KANAN":
        keyboard.press(Key.right)
        keyboard.release(Key.right)
    elif gesture == "TURUN":
        keyboard.press(Key.down)
        keyboard.release(Key.down)
    elif gesture == "LOMPAT":
        keyboard.press(Key.up)
        keyboard.release(Key.up)

# Main loop
while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Gagal membaca dari webcam.")
        break
    
    # Ubah format warna ke RGB untuk MediaPipe
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    
    # Proses deteksi tangan
    results = hands.process(image)
    
    # Ubah kembali format warna untuk OpenCV
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # Gambar landmarks tangan
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Deteksi gestur
            current_time = time.time()
            if current_time > gesture_cooldown:
                gesture = detect_gesture(hand_landmarks)
                if gesture and gesture != last_gesture:
                    print(f"Gesture Terdeteksi: {gesture}")
                    press_key(gesture)
                    last_gesture = gesture
                    gesture_cooldown = current_time + cooldown_time
    
    # Flip horizontal untuk tampilan yang lebih intuitif
    image = cv2.flip(image, 1)
    
    # Tampilkan informasi di layar
    # cv2.putText(image, 'Gestur 1: Arrow Left', (10, 30), 
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    # cv2.putText(image, 'Gestur 2: Arrow Right', (10, 60), 
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    # cv2.putText(image, 'Mengepal: Arrow Down', (10, 90), 
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    # cv2.putText(image, 'Membuka: Arrow Up', (10, 120), 
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Tampilkan gesture yang terdeteksi
    if last_gesture:
        cv2.putText(image, f'Gesture: {last_gesture}', (10, 150), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Tampilkan jendela hasil
    cv2.imshow('subwaysurfers_opencv', image)
    
    # Cara keluar: tekan ESC
    if cv2.waitKey(5) & 0xFF == 27:
        break

# Bersihkan resources
cap.release()
cv2.destroyAllWindows()