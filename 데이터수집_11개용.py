import json
import os
import datetime
import keyboard  # pip install keyboard
import serial

# -----------------------------------
ser = serial.Serial("COM7", 9600, timeout=1)
print(f"PORT: COM7, BAUD: 9600")
# -----------------------------------

# 전역 데이터 저장
all_data = {}  # {"단어명": [ {trial, frame, name, sensor}, ... ]}

# ===== 경로 설정 =====
SAVE_DIR = "C:/Users/pjimi/project/arduino_hand/hand_language_data"
os.makedirs(SAVE_DIR, exist_ok=True)

# ============================
# 유틸리티 함수
# ============================

def parse_sensor_line(line: str):
    """라인에서 ',' 구분 숫자 11개만 뽑아 리스트로 반환"""
    parts = line.strip().split(',')
    if len(parts) != 11:
        print(f"[경고] 센서값 개수 불일치: {len(parts)}개 (11개 필요) | raw: {line}")
        return []
    try:
        vals = [int(x) for x in parts]
        return vals
    except:
        print(f"[경고] 센서값 변환 실패 | raw: {line}")
        return []

def save_trial_to_file(word, trial_data):
    """한 시행(trial) 데이터를 해당 수화 JSON 파일에 저장"""
    filename = os.path.join(SAVE_DIR, f"{word}.json")

    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    existing_data.append(trial_data)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)

    # 메모리에도 반영
    if word not in all_data:
        all_data[word] = []
    all_data[word].append(trial_data)

def get_next_trial_number(word):
    """기존 JSON 파일을 열어 해당 단어의 마지막 trial 번호를 가져와 +1 리턴"""
    filename = os.path.join(SAVE_DIR, f"{word}.json")
    if not os.path.exists(filename):
        return 1
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not data:
            return 1
        last_trial = data[-1][0]["trial"]  # trial_data는 리스트 형태
        return last_trial + 1
    except:
        return 1

def collect_mode(word, trial_num):
    """스페이스바 누르고 있는 동안 센서값 수집"""
    print(f"\n=== {word} 단어 시행 {trial_num} ===")
    print("스페이스바를 눌러 수집 시작, 떼면 수집 종료")

    trial_data = []
    frame_num = 1

    try:
        while True:
            if keyboard.is_pressed('space'):
                line = ser.readline().decode(errors="ignore").strip()
                if not line:
                    continue
                sensor_vals = parse_sensor_line(line)
                if len(sensor_vals) != 11:
                    continue

                frame_dict = {
                    "trial": trial_num,
                    "frame": frame_num,
                    "name": word,
                    "sensor": sensor_vals
                }
                trial_data.append(frame_dict)
                frame_num += 1
                print(f"\r프레임 수집 중: {frame_num - 1}", end="")
            else:
                if trial_data:
                    print("\n스페이스바 떼짐. 수집 종료")
                    while True:
                        choice = input("이 시행 데이터를 저장하시겠습니까? (y/n): ").strip().lower()
                        if choice == 'y':
                            save_trial_to_file(word, trial_data)
                            print(f"시행 {trial_num} 저장 완료\n")
                            return
                        elif choice == 'n':
                            print(f"시행 {trial_num} 데이터 삭제됨\n")
                            return
                        else:
                            print("y 또는 n으로 입력해주세요.")
                else:
                    continue
    except KeyboardInterrupt:
        print("\n수집 중단됨. 현재 프레임은 저장되지 않음.")

def export_final_file():
    """선택한 수화의 모든 시행 데이터를 합친 최종 파일 생성"""
    word = input("최종 파일을 출력할 수화를 입력하세요: ").strip()
    if word not in all_data or not all_data[word]:
        print(f"[오류] {word}에 대한 데이터가 없습니다.")
        return

    final_filename = os.path.join(
        SAVE_DIR,
        f"{word}_final_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )

    with open(final_filename, 'w', encoding='utf-8') as f:
        json.dump(all_data[word], f, indent=4, ensure_ascii=False)
    print(f"{final_filename} 파일 생성 완료!\n")

def load_existing_data():
    """기존 JSON 파일들을 all_data에 불러오기"""
    for filename in os.listdir(SAVE_DIR):
        if filename.endswith(".json") and "_final_data_" not in filename:
            word = filename.replace(".json", "")
            filepath = os.path.join(SAVE_DIR, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    all_data[word] = json.load(f)
            except Exception as e:
                print(f"[경고] {filename} 로드 실패: {e}")
    print(f"[로드 완료] {len(all_data)}개 단어 데이터 불러옴.")

# ============================
# 메인 메뉴
# ============================

def main_menu():
    load_existing_data()  # 🔥 프로그램 시작 시 자동으로 기존 데이터 불러오기

    while True:
        print("\n==== 수화 데이터 수집 시스템 ====")
        print("1. 수화 데이터 수집")
        print("2. 최종 파일 생성")
        print("3. 종료")
        choice = input("선택: ").strip()

        if choice == '1':
            word = input("수화 이름을 입력하세요: ").strip()
            trial_number = get_next_trial_number(word)
            print(f"자동 설정된 시행 번호: {trial_number}")
            collect_mode(word, trial_number)
        elif choice == '2':
            export_final_file()
        elif choice == '3':
            print("프로그램을 종료합니다.")
            break
        else:
            print("1, 2, 3 중 하나를 선택해주세요.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n프로그램 종료")
