from src.play import play_first_strike, play_manual, play_entropy
from src.word_list import get_word_list
from src.power_words import PowerWords
import json
import random


def save_json(filename: str, words: list[str]):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=4)
    print(f"✅ Đã xuất {filename}")

def main():
    # Lấy toàn bộ từ 5 ký tự từ corpus nltk
    all_words = get_word_list(5)

    # Tính power
    pw = PowerWords(all_words)

    # Chỉ lấy phần word thôi (bỏ power)
    top_50 = [w for w, _ in pw.word_list[:50]]
    bottom_50 = [w for w, _ in pw.word_list[-50:]]
    random_50 = [w for w, _ in random.sample(pw.word_list, 50)]

    # Xuất ra 3 file JSON riêng
    save_json("high_power.json", top_50)
    save_json("low_power.json", bottom_50)
    save_json("random_power.json", random_50)

if __name__ == "__main__":
    main()
# if __name__ == "__main__":
#     words = get_word_list()
#     print(f"Đã tải {len(words)} từ có độ dài 5 chữ cái.")

#     # --- Chọn chiến lược bạn muốn chạy ---

#     # 1. Chơi với chiến lược "Đòn phủ đầu"
#     # print("\n--- Bắt đầu chơi với chiến lược 'Đòn phủ đầu' ---")
#     # play_first_strike(words)

#     # 2. Chơi với chiến lược "Entropy"
#     print("\n--- Bắt đầu chơi với chiến lược 'Entropy' ---")
#     play_entropy(words)