import unittest
import json
import io
import os
import logging
import time
from contextlib import redirect_stdout

from src.play import play_first_strike
from src.word_list import get_word_list

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# Thiết lập logger
logging.basicConfig(
    filename="tests/first_strike_test.log",
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

def load_words_from_json(filename):
    with open(os.path.join(DATA_DIR, filename), "r") as f:
        return json.load(f)

def timed_run(func, *args, **kwargs):
    """Chạy func và trả về (kết quả, thời gian chạy giây)"""
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed

class PlayFirstStrikeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.word_list = get_word_list()

    def run_test_on_dataset(self, dataset_name) -> tuple[float, float, float]:
        words = load_words_from_json(dataset_name)
        total_tries = 0
        total_fails = 0

        f = io.StringIO()
        total_time = 0.0
        for target in words:
            # Sửa play_first_strike để trả về số lượt đoán và trạng thái thành công/thất bại
            with redirect_stdout(f):  # Chặn mọi print bên trong play_first_strike
                result, elapsed = timed_run(play_first_strike, self.word_list, target_word=target, max_attempts=6)
            total_time += elapsed
            if result and result <= 6:
                print(f"Target: {target}, Attempts: {result}")
                total_tries += result
            else:
                total_tries += 6 # Khi thua vẫn cộng vào số lượt đoán
                total_fails += 1

        avg_tries = total_tries / len(words)
        success_rate =  (len(words) - total_fails) / len(words)
        avg_time = total_time / len(words)
        return avg_tries, success_rate, avg_time

    def test_repeat_letter(self):
        result = self.run_test_on_dataset("repeat-letter.json")

        avg_tries = round(result[0], 2)
        success_rate = round(result[1] * 100, 2)
        avg_time = round(result[2], 4)

        logger.info(f"<<<Repeat Letter>>>> avg tries: {avg_tries}")
        logger.info(f"<<<Repeat Letter>>>> success rate: {success_rate} %")
        logger.info(f"<<<Repeat Letter>>>> avg time: {avg_time} s")
        print(f"<<<Repeat Letter>>>> Số lượt đoán trung bình: {avg_tries}")
        print(f"<<<Repeat Letter>>>> success rate: {success_rate} %")
        print(f"<<<Repeat Letter>>>> Thời gian trung bình: {avg_time} s")
        print()

    def test_high_power(self):
        result = self.run_test_on_dataset("high-power.json")

        avg_tries = round(result[0], 2)
        success_rate = round(result[1] * 100, 2)
        avg_time = round(result[2], 4)

        logger.info(f"<<<High Power>>>> avg tries: {avg_tries}")
        logger.info(f"<<<High Power>>>> success rate: {success_rate} %")
        logger.info(f"<<<High Power>>>> avg time: {avg_time} s")
        print(f"<<<High Power>>>> Số lượt đoán trung bình: {avg_tries}")
        print(f"<<<High Power>>>> success rate: {success_rate} %")
        print(f"<<<High Power>>>> Thời gian trung bình: {avg_time} s")
        print()

    def test_low_power(self):
        result = self.run_test_on_dataset("low-power.json")

        avg_tries = round(result[0], 2)
        success_rate = round(result[1] * 100, 2)
        avg_time = round(result[2], 4)

        logger.info(f"<<<Low Power>>>> avg tries: {avg_tries}")
        logger.info(f"<<<Low Power>>>> success rate: {success_rate} %")
        logger.info(f"<<<Low Power>>>> avg time: {avg_time} s")
        print(f"<<<Low Power>>>> Số lượt đoán trung bình: {avg_tries}")
        print(f"<<<Low Power>>>> success rate: {success_rate} %")
        print(f"<<<Low Power>>>> Thời gian trung bình: {avg_time} s")
        print()

    def test_random_letter(self):
        result = self.run_test_on_dataset("random.json")

        avg_tries = round(result[0], 2)
        success_rate = round(result[1] * 100, 2)
        avg_time = round(result[2], 4)

        logger.info(f"<<<Random Letter>>>> avg tries: {avg_tries}")
        logger.info(f"<<<Random Letter>>>> success rate: {success_rate} %")
        logger.info(f"<<<Random Letter>>>> avg time: {avg_time} s")
        print(f"<<<Random Letter>>>> Số lượt đoán trung bình: {avg_tries}")
        print(f"<<<Random Letter>>>> success rate: {success_rate} %")
        print(f"<<<Random Letter>>>> Thời gian trung bình: {avg_time} s")
        print()

if __name__ == "__main__":
    unittest.main(buffer=True)