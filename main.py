import argparse

from src.play import play_first_strike, play_manual
from src.word_list import get_word_list

parser = argparse.ArgumentParser(
    description="Game wordle cực hay!"
)

parser.add_argument("--target", type=str, default="happy", help="Chọn từ cần đoán")

if __name__ == "__main__":
    words = get_word_list()
    print(f"Đã tải {len(words)} từ có độ dài 5 chữ cái.")

    args = parser.parse_args()
    if len(args.target) != 5:
        raise ValueError("Từ cần đoán phải có độ dài 5 chữ cái")

    play_manual(word_list=words, target_word=args.target)
    # play_first_strike(words, target_word=args.target)
