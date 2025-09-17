from collections import defaultdict, Counter


class FrequencyKnowledge:
    """
    Lưu trữ thông tin về tần suất xuất hiện của các ký tự trong từ cần đoán.
    """

    def __init__(self, word_length=5):
        # Một danh sách có các ký tự đúng vị trí hoặc None
        #   Ví dụ: Nếu từ cần đoán là `"teach"`, sau khi đoán `"teeth"` và biết
        #   "t" đúng vị trí 0, "e" đúng vị trí 1, "h" đúng vị trí 4, thì:
        #   => `correct = ['t', 'e', None, None, 'h']
        self.correct = [None] * word_length

        # Một danh sách có chứa một bộ ký tự không đúng vị trí hoặc None
        #   Ví dụ: Nếu từ cần đoán là `"teach"`, sau khi đoán `"table"` và biết
        #   "e" sai tại vị trí 5, "a" sai vị trí tại vị trí 2, thì:
        #   => `wrong_pos = [set(), set('a'), set(), set(), set('e')]
        self.wrong_pos = [set() for _ in range(word_length)]

        # Tập hợp các chữ chắc chắn không xuất hiện trong từ
        self.excluded = set()

        # Một từ điển chứa [ký tự]: [số lượng tối thiểu phải có], cho biết số
        # lượng từ đã đoán được đó bắt buộc phải có ít nhất `n` lần
        #   Ví dụ: Nếu từ cần đoán là `"teeth"`, sau khi đoán `"tenth"`, thì ta
        #   biết "t" xuất hiện ít nhất 2 và "e" đều xuất hiện ít 1 lần
        #   => `must_have['t'] = 2`, `must_have['e'] = 1`.
        self.must_have = defaultdict(int)

        # Một từ điển chứa [ký tự]: [số lượng tối đa có thể có], cho biết số
        # lượng từ đã đoán được đó có thể có tối đa `n` lần
        #   Ví dụ: Nếu từ cần đoán là `"teach"`, sau khi đoán `"teeth"`, thì ta
        #   biết được "e" chỉ xuất hiện tối đa 1 lần, không phải 2
        #   => `max_count['e'] = 1`
        self.max_count = defaultdict(lambda: None)

    def update(self, guess, result):
        """Cập nhật thông tin từ từ đoán mới"""

        # Đếm số lần xuất hiện của từng ký tự trong guess và result
        green_counter = Counter()  # Đếm số lần xuất hiện ký tự xanh
        yellow_counter = Counter()  # Đếm số lần xuất hiện ký tự vàng

        # Lần 1: Đánh dấu green, cập nhật correct và must_have
        for i, (char, charResult) in enumerate(zip(guess, result)):
            if charResult == "G":
                self.correct[i] = char
                green_counter[char] += 1
                self.must_have[char] = max(self.must_have[char], green_counter[char])

        # Lần 2: Đánh dấu yellow, cập nhật wrong_pos và must_have
        for i, (char, charResult) in enumerate(zip(guess, result)):
            if charResult == "Y":
                self.wrong_pos[i].add(char)
                yellow_counter[char] += 1
                self.must_have[char] = max(
                    self.must_have[char], green_counter[char] + yellow_counter[char]
                )

        # Lần 3: Đánh dấu gray, cập nhật excluded và max_count
        for i, (char, charResult) in enumerate(zip(guess, result)):
            if charResult == "X":
                # Nếu ký tự này đã có trong must_have, thì max_count = must_have[g]
                if self.must_have[char]:
                    self.max_count[char] = self.must_have[char]
                else:
                    self.excluded.add(char)
                    self.max_count[char] = 0

    def is_possible(self, word):
        # Kiểm tra một từ có phù hợp với knowledge hiện tại không
        word_counter = Counter(word)

        # Chỉ đoán từ có những chữ cái khớp với vị trí của "chữ cái đúng vị trí" (self.correct)
        for i, char in enumerate(self.correct):
            if char and word[i] != char:
                return False

        # Chỉ đoán những từ có những chứ cái khác vị trí với "chữ cái đúng nhưng sai vị trí" (self.wrong_pos)
        for i, s in enumerate(self.wrong_pos):
            if word[i] in s:
                return False

        # Không đoán những từ có chứa chữ cái đã bị loại bỏ (self.excluded)
        for char in self.excluded:
            if char in word:
                return False

        # Chỉ đoán những từ có chứa số lượng chữ cái tối thiểu đã được xác định (self.must_have)
        for char, min_count in self.must_have.items():
            if word_counter[char] < min_count:
                return False

        # Chỉ đoán những từ có chứa số lượng chữ cái tối đa đã được xác định (self.max_count)
        for char, max_count in self.max_count.items():
            if max_count is not None and word_counter[char] > max_count:
                return False

        return True
