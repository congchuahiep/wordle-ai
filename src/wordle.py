from random import choice
from typing import List, Literal, TypedDict


class WordResult(TypedDict):
    """
    Kết quả của một lần đoán từ

    Attributes:
        word: Từ đã đoán
        result: Kết quả đoán từng chữ cái
            "G" - Chữ cái đúng và đúng vị trí (Green)
            "Y" - Chữ cái đúng nhưng sai vị trí (Yellow)
            "X" - Chữ cái không có trong từ (Gray)
    """

    word: str
    results: List[Literal["G", "Y", "X"]]


class Wordle:
    word_list: list[str]  # Danh sách các từ có thể chọn
    word_length: int  # Độ dài của từ (mặc định là 5)

    # Dữ liệu để theo dõi trạng thái trò chơi
    target_word: str  # Từ cần đoán
    guessed_words: list[WordResult]  # Danh sách các từ đã đoán và kết quả của chúng
    current_attempt: int  # Lần đoán hiện tại (bắt đầu từ 1 -> max)
    max_attempts: int  # Số lần đoán tối đa

    is_won: bool

    def __init__(
        self,
        word_list: list[str],
        target_word: str | None,
        word_length: int = 5,
        max_attempts: int = 6,
    ) -> None:
        # Dữ liệu khởi tạo trò chơi
        self.word_list = word_list
        self.current_attempt = 1
        self.max_attempts = max_attempts
        self.word_length = word_length
        self.guessed_words = []
        self.is_won = False

        # Từ cần đoán
        if target_word and target_word not in word_list:
            raise ValueError(
                f"Từ mục tiêu không hợp lệ! Nó phải nằm trong danh sách từ. Từ không đúng hiện tại: {target_word}"
            )
        self.target_word = target_word if target_word else choice(self.word_list)

    def guess(self, word: str) -> WordResult | None:
        """
        Đoán một từ và nhận kết quả

        Nếu số lần đoán đã đạt đến giới hạn, trả về None
        """
        if self.current_attempt > self.max_attempts:
            return None

        if word not in self.word_list:
            raise ValueError("Từ không hợp lệ.")

        result: WordResult = {"word": word, "results": ["X"] * self.word_length}
        target_chars = list(self.target_word)
        used = [False] * self.word_length  # Đánh dấu ký tự đã dùng trong target_word

        # Lần 1: Đánh dấu "G"
        for i, char in enumerate(word):
            if char == target_chars[i]:
                result["results"][i] = "G"
                used[i] = True  # Đã dùng ký tự này

        # Lần 2: Đánh dấu "Y"
        for i, char in enumerate(word):
            if result["results"][i] == "G":
                continue
            for j, t_char in enumerate(target_chars):
                if not used[j] and char == t_char:
                    result["results"][i] = "Y"
                    used[j] = True
                    break
            # Nếu không tìm thấy, giữ nguyên là "X"

        self.guessed_words.append(result)
        self.current_attempt += 1

        if result["results"] == ["G"] * self.word_length:
            self.is_won = True

        return result
