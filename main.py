from src.word_list import get_word_list
from src.power_words import PowerWords
import json
import random
import argparse
from src.play import play_manual
from src.play import play_first_strike
from src.play import play_entropy

parser = argparse.ArgumentParser(description="Game wordle cực hay!")

parser.add_argument("--target", type=str, default="happy", help="Chọn từ cần đoán")


def save_json(filename: str, words: list[str]):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=4)
    print(f"✅ Đã xuất {filename}")


# def main():
#     # Lấy toàn bộ từ 5 ký tự từ corpus nltk
#     all_words = get_word_list(5)

#     # Tính power
#     pw = PowerWords(all_words)

#     # Chỉ lấy phần word thôi (bỏ power)
#     top_50 = [w for w, _ in pw.word_list[:50]]
#     bottom_50 = [w for w, _ in pw.word_list[-50:]]
#     random_50 = [w for w, _ in random.sample(pw.word_list, 100)]

#     # Xuất ra 3 file JSON riêng
#     save_json("high_power.json", top_50)
#     save_json("low_power.json", bottom_50)
#     save_json("random_power.json", random_50)


if __name__ == "__main__":
    words = get_word_list()
    print(f"Đã tải {len(words)} từ có độ dài 5 chữ cái.")

    args = parser.parse_args()
    if len(args.target) != 5:
        raise ValueError("Từ cần đoán phải có độ dài 5 chữ cái")

    # --- Chế độ chơi ---
    mode = input(
        "Chọn chế độ chơi ([Enter]: thủ công, [1] AI - Đòn phủ đầu, [2] AI - Entropy): "
    )
    if mode == "1":
        # 1. Chơi với chiến lược "Đòn phủ đầu"
        print("\n--- Bắt đầu chơi với chiến lược 'Đòn phủ đầu' ---")
        play_first_strike(words, target_word=args.target)
    elif mode == "2":
        # 2. Chơi với chiến lược "Entropy"
        print("\n--- Bắt đầu chơi với chiến lược 'Entropy' ---")
        play_entropy(words, target_word=args.target)
    else:
        play_manual(word_list=words, target_word=args.target)
