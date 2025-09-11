from random import choice

from .power_words import PowerWords

from .wordle import Wordle


def play_manual(word_list: list[str]) -> str:
    """
    Chơi thủ công

    Args:
        word_list (list[str]): Danh sách các từ có thể chọn.

    Returns:
        str: Từ được chọn để chơi.
    """
    while True:
        user_input = input("Nhập từ bạn muốn chơi (5 chữ cái): ").strip().lower()
        if len(user_input) != 5:
            print("Vui lòng nhập đúng 5 chữ cái.")
        elif user_input not in word_list:
            print("Từ không hợp lệ. Vui lòng thử lại.")
        else:
            return user_input


def play_first_strike(
    word_list: list[str], target_word: str | None, max_attempts: int = 6
):
    """
    Chơi wordle từ động với chiến thuật "Đòn phủ đầu" - "First Strike"

    Args:
        word_list (list[str]): Danh sách các từ có thể chọn.

    Returns:
        str: Từ được chọn để chơi.
    """
    # Khởi tạo trò chơi
    power_words = PowerWords(word_list)
    game = Wordle(word_list, target_word=target_word, max_attempts=max_attempts)
    knowledges = {
        "excluded": [],  # Các chữ cái chắc chắn không có trong từ cần đoán
        "wrong_pos": [set() for _ in range(5)],  # Các ký tự sai vị trí (có thể lặp)
        "correct": [None] * 5,  # Các ký tự đúng vị trí
    }

    # Chọn từ có sức mạnh cao nhất để đoán đầu tiên
    best_word = choice(power_words[:20])
    last_index = -1
    result = game.guess(best_word[0])

    print(f"Đoán từ: {best_word} -> Kết quả: {''.join(result['results'])}")

    while result["word"] != game.target_word and game.attempts > 0:
        print(f"Số lần đoán còn lại: {game.attempts}")

        # Cập nhật kiến thức dựa trên kết quả đoán
        for i, res in enumerate(result["results"]):
            char = result["word"][i]
            if res == "G":
                # Nếu trước đó char từng là correct ở vị trí khác mà giờ đoán sai, loại bỏ khỏi correct
                knowledges["correct"][i] = char
                # Loại bỏ char khỏi wrong_pos ở tất cả các vị trí
                for s in knowledges["wrong_pos"]:
                    s.discard(char)

            elif res == "Y":
                # Nếu char từng là correct ở vị trí này nhưng giờ đoán sai, loại bỏ khỏi correct
                if knowledges["correct"][i] == char:
                    knowledges["correct"][i] = None
                knowledges["wrong_pos"][i].add(char)

            else:  # res == "N"
                # Chỉ thêm vào excluded nếu char không nằm trong correct hoặc wrong_pos ở vị trí khác
                if char not in knowledges["correct"] and all(
                    char not in s for s in knowledges["wrong_pos"]
                ):
                    knowledges["excluded"].append(char)

        # Lấy một từ tiếp theo để đoán dựa trên kiến thức đã có:
        # - Giữ nguyên vị trí của các chữ cái đúng
        # - Thay đổi vị trí của các chữ cái sai vị trí
        # - Loại bỏ các từ có chứa chữ cái đã biết là không có trong từ cần
        for index, word in enumerate(power_words, start=last_index + 1):
            # Loại bỏ các từ có chứa chữ cái đã biết là không có trong từ cần
            if any(char in word[0] for char in knowledges["excluded"]):
                continue

            match = True
            for i, char in enumerate(word[0]):
                # Nếu chữ cái đã đúng vị trí nhưng không khớp -> bỏ qua từ này
                if knowledges["correct"][i] and char != knowledges["correct"][i]:
                    match = False
                    break
                # Nếu chữ cái sai vị trí vẫn ở vị trí sai -> bỏ qua từ này
                if knowledges["wrong_pos"][i] and char in knowledges["wrong_pos"][i]:
                    match = False
                    break

            if match:
                print(f"Từ đoán tiếp theo: {word}")
                best_word = word
                last_index = index
                print(f"Chọn từ thứ {last_index + 1} trong danh sách từ mạnh.")
                break

        result = game.guess(best_word[0])
        print(f"Đoán từ: {best_word} -> Kết quả: {''.join(result['results'])}")
        if result["word"] == game.target_word:
            print(f"Chúc mừng! Bạn đã đoán đúng từ '{game.target_word}'")

    print(f"Từ cần đoán là: {game.target_word}")
    print(f"Số lần đoán còn lại: {game.attempts}")
    if game.attempts == 0 and result["word"] != game.target_word:
        print("Bạn đã hết lượt đoán. Chơi lại nhé!")
