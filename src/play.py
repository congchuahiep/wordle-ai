from random import choice

from .knowledge import FrequencyKnowledge

from .power_words import PowerWords

from .wordle import Wordle


def play_manual(word_list: list[str], target_word: str) -> str:
    """
    Chơi thủ công

    Args:
        word_list (list[str]): Danh sách các từ có thể chọn.

    Returns:
        str: Từ được chọn để chơi.
    """
    game = Wordle(word_list, target_word=target_word)

    while True:
        user_input = input("Nhập từ bạn muốn chơi (5 chữ cái): ").strip().lower()
        if len(user_input) != 5:
            print("Vui lòng nhập đúng 5 chữ cái.")
        elif user_input not in word_list:
            print("Từ không hợp lệ. Vui lòng thử lại.")
        else:
            result = game.guess(user_input)
            print(result)


def play_first_strike(word_list, target_word, max_attempts=6, verbose=True):
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
