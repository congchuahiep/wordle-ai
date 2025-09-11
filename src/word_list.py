import nltk
from nltk.corpus import words


def get_word_list(word_length: int = 5) -> list[str]:
    """
    Hàm này trả về danh sách các từ tiếng Anh có độ dài 5 ký tự.
    Nếu chưa có dữ liệu từ corpus, nó sẽ tự động tải về.

    Danh sách các từ này sẽ được lưu tại `%%APPDATA%%/nltk_data/corpora/words`.
    """
    word_list = []

    try:
        # Lấy danh sách các từ tiếng Anh có độ dài 5 ký tự
        # Nếu từ đó là tên riêng (bắt đầu bằng chữ hoa) thì sẽ bỏ qua
        word_list = [
            x.lower()
            for x in words.words()
            if (len(x) == word_length and not x[0].isupper())
        ]
    except LookupError:
        # Nếu words corpus chưa có dữ liệu, tải nó về máy
        nltk.download("words")
        word_list = [
            x.lower()
            for x in words.words()
            if (len(x) == word_length and not x[0].isupper())
        ]

    return word_list
