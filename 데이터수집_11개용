import json
import os
import datetime
import keyboard  # pip install keyboard

# -----------------------------------
# 기존에 ser = serial.Serial(...) 로 연결되어 있어야 함
# -----------------------------------

# 전역 데이터 저장
all_data = {}  # 수화별 누적 데이터, 예: {"고생":[{trial,frame,name,sensor},...]}

def parse_sensor_line(line: str):
    """라인에서 ',' 구분 숫자 11개만 뽑아 리스트로 반환 (오른손 전용)"""
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
    # ===== 파일 경로 입력 =====
    save_dir = ""  # 여기에 원하는 경로 입력 예: "D:/수화데이터"
    os.makedirs(save_dir, exist_ok=True)

    filename = os.path.join(save_dir, f"{word}.json")  # 단어별 파일

    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    existing_data.append(trial_data)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)

    # 메모리에도 저장
    if word not in all_data:
        all_data[word] = []
    all_data[word].append(trial_data)

def collect_mode(word, trial_num):
    """스페이스바 누르고 있는 동안 센서값 수집 (오른손 11개 기준)"""
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
                print(f"\r프레임 수집 중: {frame_num-1}", end="")
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

    # ===== 파일 경로 입력 =====
    save_dir = ""  # 여기에 원하는 경로 입력 예: "D:/수화데이터"
    os.makedirs(save_dir, exist_ok=True)

    final_filename = os.path.join(save_dir, f"{word}_final_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

    with open(final_filename, 'w', encoding='utf-8') as f:
        json.dump(all_data[word], f, indent=4, ensure_ascii=False)
    print(f"{final_filename} 파일 생성 완료!\n")

def main_menu():
    trial_counter = {}  # 단어별 trial 번호 카운트

    while True:
        print("\n==== 수화 데이터 수집 시스템 ====")
        print("1. 수화 데이터 수집")
        print("2. 최종 파일 생성")
        print("3. 종료")
        choice = input("선택: ").strip()

        if choice == '1':
            word = input("수화 이름을 입력하세요: ").strip()
            trial_num = trial_counter.get(word, 1)
            print(f"{word} 단어의 {trial_num}번째 시행 수집 예정")
            collect_mode(word, trial_num)
            trial_counter[word] = trial_num + 1
        elif choice == '2':
            export_final_file()
        elif choice == '3':
            print("프로그램 종료")
            break
        else:
            print("1, 2, 3 중에서 선택해주세요.")

# -----------------------------------
# 기존 while True 루프 아래에 붙여서 실행
# -----------------------------------
if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n프로그램 종료")
