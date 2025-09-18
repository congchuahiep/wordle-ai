from random import choice

from .knowledge import FrequencyKnowledge

from .power_words import PowerWords

from .wordle import Wordle

import math

from collections import defaultdict


def play_manual(word_list: list[str], target_word: str) -> str:
    """
    Chơi thủ công

    Args:
        word_list (list[str]): Danh sách các từ có thể chọn.

    Returns:
        str: Từ được chọn để chơi.
    """
    game = Wordle(word_list, target_word=target_word)

    while game.current_attempt <= game.max_attempts and not game.is_won:
        user_input = input("Nhập từ bạn muốn đoán (5 chữ cái): ").strip().lower()
        if len(user_input) != 5:
            print("Vui lòng nhập đúng 5 chữ cái.")
        elif user_input not in word_list:
            print("Từ không hợp lệ. Vui lòng thử lại.")
        else:
            result = game.guess(user_input)
            print(result)

    if game.is_won:
        print(
            f"Chúc mừng! Bạn đã đoán đúng từ {game.target_word} sau {game.current_attempt - 1} lần."
        )
    else:
        print(f"Rất tiếc, bạn đã hết lượt. Từ đúng là {game.target_word}.")


def play_first_strike(
    word_list: list[str], target_word: str = None, max_attempts: int = 6, verbose=True
):
    """
    Chơi wordle tự động với chiến thuật "First Strike" dựa trên power_words và knowledge frequency-based.

    Args:
        word_list (list[str]): Danh sách các từ có thể chọn.
        verbose (bool): In thông tin chi tiết về quá trình chơi.

    Returns:
        str: Từ được chọn để chơi.
    """
    power_words = PowerWords(word_list)
    game = Wordle(word_list, target_word=target_word, max_attempts=max_attempts)
    knowledge = FrequencyKnowledge(word_length=5)

    # Chọn từ đầu tiên (Luôn chọn từ nằm trong top 50)
    best_word = choice(power_words[:50])[0]
    result = game.guess(best_word)
    if verbose and result:
        print(f"Đoán từ: {best_word} -> Kết quả: {''.join(result['results'])}")

    last_index = -1
    while (
        result
        and result["word"] != game.target_word
        and game.current_attempt <= max_attempts
    ):
        # Cập nhật knowledge
        knowledge.update(result["word"], result["results"])

        # Duyệt power_words từ trên xuống, chọn từ đầu tiên thỏa knowledge
        found = False
        for index, power_word in enumerate(power_words, start=last_index + 1):
            candidate = power_word[0]
            if knowledge.is_possible(candidate):
                best_word = candidate
                last_index = index
                found = True
                if verbose:
                    print(
                        f"Từ đoán tiếp theo: {best_word} (thứ {index + 1} trong power_words)"
                    )
                break
        if not found:
            if verbose:
                print("Không còn từ nào phù hợp knowledge!")
            break

        result = game.guess(best_word)
        if verbose and result:
            print(f"Đoán từ: {best_word} -> Kết quả: {''.join(result['results'])}")

    if verbose and result:
        if result["word"] == game.target_word:
            print(
                f"Chúc mừng! Bạn đã đoán đúng từ '{game.target_word}' sau {game.current_attempt - 1} lượt."
            )
        else:
            print(f"Bạn đã hết lượt đoán. Từ đúng là: {game.target_word}")

    # Trả về số lượt đoán nếu thành công, hoặc max_attempts nếu thất bại
    return (
        game.current_attempt - 1
        if result and result["word"] == game.target_word
        else max_attempts
    )


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


def find_best_entropy_guess(
    possible_answers: list[str], all_valid_guesses: list[str]
) -> str:
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

    print(
        f"Đã tính toán xong. Từ tốt nhất là '{best_guess}' với điểm Entropy: {max_entropy:.4f}"
    )
    return best_guess


def play_entropy(word_list: list[str], target_word: str = None, max_attempts: int = 6):
    """
    Chơi wordle tự động với chiến thuật Entropy
    Lượt đầu tiên sử dụng Power Word để tối ưu tốc độ.
    Các lượt sau, AI chỉ được phép chọn từ đoán nằm trong danh sách các đáp án
    tiềm năng còn lại để tối đa hóa cơ hội chiến thắng.
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
        print(f"Lượt {game.current_attempt}")
        print(f"Số lượng đáp án khả thi còn lại: {len(possible_answers)}")

        # --- LỰA CHỌN TỪ ĐOÁN ---
        # Lượt đầu tiên: Dùng Power Word
        if game.current_attempt == 1:
            print("Lượt 1: Chọn Power Word mạnh nhất.")
            current_guess = power_words[0][0]
        # Các lượt sau: Dùng Entropy (Hard Mode)
        else:
            print("Đang tính toán từ có Entropy cao nhất (Hard Mode)...")
            # --- ĐIỂM THAY ĐỔI QUAN TRỌNG ---
            # Không gian tìm kiếm (search_space) chính là danh sách các đáp án còn lại.
            # Điều này buộc AI phải chọn một từ có khả năng là đáp án đúng.
            current_guess = find_best_entropy_guess(possible_answers, possible_answers)

        # --- THỰC HIỆN ĐOÁN VÀ LẤY KẾT QUẢ ---
        result = game.guess(current_guess)
        # Kiểm tra nếu result là None (trường hợp hết lượt)
        if result is None:
            break
            
        feedback = "".join(result["results"])
        print(f"Đoán từ: '{current_guess}' -> Kết quả: {feedback}")

        # --- KIỂM TRA ĐIỀU KIỆN THẮNG ---
        if current_guess == game.target_word:
            print(
                f"Chúc mừng! Bạn đã đoán đúng từ '{game.target_word}' sau {game.current_attempt} lần đoán."
            )
            # Trả về số lượt đoán khi thắng
            return game.current_attempt - 1 

        # --- CẬP NHẬT DANH SÁCH ĐÁP ÁN KHẢ THI ---
        # Lọc lại danh sách possible_answers dựa trên phản hồi vừa nhận được
        new_possible_answers = []
        for word in possible_answers:
            # Từ `current_guess` vừa đoán phải khác `word` đang xét, trừ khi nó là từ duy nhất còn lại
            if word == current_guess:
                continue
            if simulate_feedback(current_guess, word) == feedback:
                new_possible_answers.append(word)
        possible_answers = new_possible_answers
        
        # Nếu không còn từ nào khả thi, có lỗi logic ở đâu đó
        if not possible_answers:
             # Có thể từ đoán cuối cùng chính là đáp án, thêm nó lại
            if simulate_feedback(current_guess, game.target_word) == feedback and current_guess == game.target_word:
                 possible_answers = [current_guess]
            else:
                print("Lỗi: Không còn đáp án nào khả thi!")
                break


    # --- XỬ LÝ KHI THUA ---
    print(f"Rất tiếc, bạn đã hết lượt đoán. Từ cần tìm là '{game.target_word}'.")
    return max_attempts