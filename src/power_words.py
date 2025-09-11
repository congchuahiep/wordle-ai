class PowerWords:
    """
    Lớp này quản lý danh sách các từ cùng với "điểm mạnh" của chúng.
    "Điểm mạnh" của một từ được xác định dựa trên tần suất xuất hiện của các chữ cái trong từ đó
    trong toàn bộ danh sách từ. Từ có các chữ cái xuất hiện thường xuyên hơn sẽ có điểm mạnh cao hơn.
    """

    word_list: list[tuple[str, int]]  # Danh sách các từ cùng với điểm mạnh của chúng

    def __init__(self, word_list: list[str]) -> None:
        self.word_list = self.calculate_power_words(word_list)

    def __getitem__(self, index):
        return self.word_list[index]

    def __iter__(self):
        return iter(self.word_list)

    def calculate_power_words(self, word_list: list[str]) -> list[tuple[str, int]]:
        """
        Hàm này tính toán "điểm mạnh" của từng từ trong danh sách từ.

        "Điểm mạnh" của một từ được xác định dựa trên tần suất xuất hiện của các chữ cái trong từ đó
        trong toàn bộ danh sách từ. Từ có các chữ cái xuất hiện thường xuyên hơn sẽ có điểm mạnh cao hơn.

        Args:
            word_list (list[str]): Danh sách các từ cần tính toán điểm mạnh.

        Returns:
            list[tuple[str, int]]: Trả về một danh sách các từ được sắp xếp theo điểm mạnh từ cao đến thấp.
        """

        # Từ điển để lưu tần suất xuất hiện của từng chữ cái
        letterDict = {}

        # Danh sách các "từ" cùng với "điểm mạnh" của chúng
        powerList: list[tuple[str, int]] = []

        # Đếm tần suất xuất hiện của từng chữ cái trong toàn bộ danh sách từ
        for word in word_list:
            for letter in word:
                letter = letter.lower()
                if letter in letterDict:
                    letterDict[letter] += 1
                else:
                    letterDict[letter] = 1

        # Tính toán điểm mạnh cho từng từ (chỉ tính mỗi ký tự một lần)
        for word in word_list:
            unique_letters = set(word)
            power = sum(letterDict[letter] for letter in unique_letters)
            powerList.append((word, power))

        powerList.sort(key=lambda x: x[1], reverse=True)
        return powerList

    def find_word(self, word: str) -> tuple[str, int, int]:
        """
        Tìm một từ trong danh sách các từ có điểm mạnh.

        Args:
            word (str): Từ cần tìm.

        Returns:
            tuple[str, int] | None: Trả về từ cùng với điểm mạnh nếu tìm thấy, ngược lại trả về None.
        """
        for index, power_word in enumerate(self.word_list):
            if power_word[0] == word:
                return (power_word[0], power_word[1], index)

        return None
