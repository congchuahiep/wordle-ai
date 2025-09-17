from random import choice

from .power_words import PowerWords

from .wordle import Wordle

import math

from collections import defaultdict


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
    word_list: list[str], target_word: str = None, max_attempts: int = 6
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

    while result["word"] != game.target_word and game.current_attempt <= game.max_attempts:
        print(f"Số lần đoán còn lại: {game.max_attempts - (game.current_attempt - 1)}")

        # Cập nhật kiến thức dựa trên kết quả đoán
        for i, res in enumerate(result["results"]):
            char = result["word"][i]
            if res == "G":
                # Nếu trước đó char từng là correct ở vị trí khác mà giờ đoán sai, loại bỏ khỏi correct
                knowledges["correct"][i] = char
                # Loại bỏ char khỏi wrong_pos ở tất cả các vị trí
                for s in knowledges["wrong_pos"]:
                    s.discard(char)
                    break

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
    print(f"Số lần đoán còn lại: {game.max_attempts - (game.current_attempt - 1)}")
    if game.current_attempt > game.max_attempts and result["word"] != game.target_word:
        print("Bạn đã hết lượt đoán. Chơi lại nhé!")


def simulate_feedback(guess: str, answer: str) -> str:
    """
    Giả lập và trả về chuỗi phản hồi ('G', 'Y', 'X') cho một cặp từ đoán và từ đáp án.
    Hàm này sử dụng logic Wordle chính xác (thuật toán 2 lượt duyệt).
    """
    results = ["X"] * len(guess)
    target_letters = list(answer)

    # Lượt 1: Tìm các chữ cái đúng vị trí (Green)
    for i, char in enumerate(guess):
        if char == target_letters[i]:
            results[i] = "G"
            target_letters[i] = None  # Đánh dấu là đã sử dụng

    # Lượt 2: Tìm các chữ cái đúng nhưng sai vị trí (Yellow)
    for i, char in enumerate(guess):
        if results[i] == "G":
            continue
        if char in target_letters:
            results[i] = "Y"
            target_letters.remove(char)
            
    return "".join(results)


def find_best_entropy_guess(possible_answers: list[str], all_valid_guesses: list[str]) -> str:
    """
    Tìm từ đoán tốt nhất bằng cách tính toán Entropy.
    Từ tốt nhất là từ có khả năng phân tách danh sách các câu trả lời còn lại
    thành nhiều nhóm nhỏ nhất có thể.
    """
    # Nếu chỉ còn 1 hoặc 2 từ, đoán luôn từ đầu tiên để có cơ hội thắng
    if len(possible_answers) <= 2:
        return possible_answers[0]

    best_guess = ""
    max_entropy = -1

    # Duyệt qua tất cả các từ có thể dùng để đoán
    for guess_word in all_valid_guesses:
        partitions = defaultdict(list)
        
        # Với mỗi từ đoán, giả lập kết quả với tất cả các đáp án còn lại
        for answer in possible_answers:
            pattern = simulate_feedback(guess_word, answer)
            partitions[pattern].append(answer)
        
        # Tính toán entropy cho từ đoán hiện tại
        current_entropy = 0.0
        total_answers = len(possible_answers)
        for pattern in partitions:
            p = len(partitions[pattern]) / total_answers
            current_entropy += -p * math.log2(p)
            
        # Cập nhật từ đoán tốt nhất
        if current_entropy > max_entropy:
            max_entropy = current_entropy
            best_guess = guess_word
            
    print(f"Đã tính toán xong. Từ tốt nhất là '{best_guess}' với điểm Entropy: {max_entropy:.4f}")
    return best_guess

def play_entropy(
    word_list: list[str], target_word: str = None, max_attempts: int = 6
):
    """
    Chơi wordle tự động với chiến thuật Entropy.
    Lượt đầu tiên sử dụng Power Word để tối ưu tốc độ, các lượt sau sử dụng Entropy
    để tối đa hóa lượng thông tin thu được.
    """
    # --- KHỞI TẠO ---
    power_words = PowerWords(word_list)
    game = Wordle(word_list, target_word=target_word, max_attempts=max_attempts)
    
    # Danh sách các từ có thể là đáp án, ban đầu là toàn bộ danh sách
    possible_answers = word_list.copy()
    current_guess = ""

    print(f"Từ cần đoán là: {game.target_word}")

    # --- VÒNG LẶP CHÍNH CỦA GAME ---
    while game.current_attempt <= 6:
        print("-" * 20)
        print(f"{game.current_attempt}")
        print(f"Số lượng đáp án khả thi còn lại: {len(possible_answers)}")

        # --- LỰA CHỌN TỪ ĐOÁN ---
        # Lượt đầu tiên: Dùng Power Word
        if game.current_attempt == 1:
            print("Lượt 1: Chọn Power Word mạnh nhất.")
            current_guess = power_words[0][0]  # Lấy từ có điểm cao nhất, ví dụ 'soare' hoặc 'slate'
        # Các lượt sau: Dùng Entropy
        else:
            print("Đang tính toán từ có Entropy cao nhất... (có thể mất một lát)")
            # all_valid_guesses có thể là word_list hoặc power_words để tăng tốc
            # Sử dụng word_list sẽ cho kết quả chính xác nhất
            current_guess = find_best_entropy_guess(possible_answers, word_list)

        # --- THỰC HIỆN ĐOÁN VÀ LẤY KẾT QUẢ ---
        result = game.guess(current_guess)
        feedback = "".join(result["results"])
        print(f"Đoán từ: '{current_guess}' -> Kết quả: {feedback}")

        # --- KIỂM TRA ĐIỀU KIỆN THẮNG ---
        if current_guess == game.target_word:
            print(f"Chúc mừng! Bạn đã đoán đúng từ '{game.target_word}' sau {game.current_attempt} lần đoán.")
            return game.current_attempt

        # --- CẬP NHẬT DANH SÁCH ĐÁP ÁN KHẢ THI ---
        # Lọc lại danh sách possible_answers dựa trên phản hồi vừa nhận được
        new_possible_answers = []
        for word in possible_answers:
            if simulate_feedback(current_guess, word) == feedback:
                new_possible_answers.append(word)
        possible_answers = new_possible_answers

    # --- XỬ LÝ KHI THUA ---
    print(f"Rất tiếc, bạn đã hết lượt đoán. Từ cần tìm là '{game.target_word}'.")