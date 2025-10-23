import serial

# 포트 이름 확인 할 것!!!
# 윈도우: 장치관리자 > 포트(COM & LPT)에서 확인 or arduino ide에서 포트 확인
PORT = "COM7"        # 본인 포트
BAUD = 9600          # 시리얼

ser = serial.Serial(PORT, BAUD, timeout=1)
print(f"PORT:{PORT}, BAUD:{BAUD}")

try:
    while True:
        line = ser.readline().decode(errors="ignore").strip()
        if line:
            print(line)
except KeyboardInterrupt:
    print("--- Interrupted ---")
finally:
    ser.close()
