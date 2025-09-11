from src.play import play_first_strike
from src.word_list import get_word_list


if __name__ == "__main__":
    words = get_word_list()
    print(f"Đã tải {len(words)} từ có độ dài 5 chữ cái.")

    play_first_strike(words, target_word="teeth")

    
