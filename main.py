from src.play import play_first_strike, play_manual, play_entropy
from src.word_list import get_word_list


if __name__ == "__main__":
    words = get_word_list()
    print(f"Đã tải {len(words)} từ có độ dài 5 chữ cái.")

    # --- Chọn chiến lược bạn muốn chạy ---

    # 1. Chơi với chiến lược "Đòn phủ đầu"
    # print("\n--- Bắt đầu chơi với chiến lược 'Đòn phủ đầu' ---")
    # play_first_strike(words)

    # 2. Chơi với chiến lược "Entropy"
    print("\n--- Bắt đầu chơi với chiến lược 'Entropy' ---")
    play_entropy(words)