from random import random
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
    attempts: int  # Số lần đoán còn lại

    def __init__(
        self,
        word_list: list[str],
        target_word: str | None,
        word_length: int = 5,
        max_attempts: int = 6,
    ) -> None:
        # Dữ liệu khởi tạo trò chơi
        self.word_list = word_list
        self.attempts = max_attempts
        self.word_length = word_length
        self.guessed_words = []

        # Từ cần đoán
        if target_word not in word_list:
            raise ValueError("Từ mục tiêu không hợp lệ! Nó phải nằm trong danh sách từ")
        self.target_word = target_word if target_word else random.choice(self.word_list)

    def guess(self, word: str) -> WordResult:
        """
        Đoán một từ và nhận kết quả
        """
        if word not in self.word_list:
            raise ValueError("Từ không hợp lệ.")

        result: WordResult = {"word": word, "results": []}

        for i, char in enumerate(word):
            if char == self.target_word[i]:
                result["results"].append("G")
            elif char in self.target_word:
                result["results"].append("Y")
            else:
                result["results"].append("X")

        self.guessed_words.append(result)
        self.attempts -= 1

        return result
