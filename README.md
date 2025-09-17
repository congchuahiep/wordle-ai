- [ ] Phân tích thuật toán
- [ ] Tạo GUI bằng *chưa biết*



## Chạy bài test

Tại đây cung cấp các file JSON chứa dữ liệu cho các chiến thuật. Gồm 3 tệp:
- `high-power.json` : Chứa các từ có những chữ cái thường gặp *(e, a, s,...)*
- `low-power.json` : Chứa các từ có những chữ cái ít gặp *(w, z, j,...)*
- `repeat-letter.json` : Chứa các từ có những chữ cái lặp lại *(aa, bb, cc,...)*

Để chạy các chiến thuật, bạn có thể sử dụng các lệnh sau:

- Chạy bài test cho chiến thuật "đòn phủ đầu"
```bash
python -m unittest -b tests.play_first_strike
```

Sau khi chạy, hệ thống sẽ tự động log các thông tin về kết quả của chiến thuật.

## Tham khảo
- [https://github.com/pranjali0921/Wordle_AI](https://github.com/pranjali0921/Wordle_AI)
- [https://github.com/djlynn03/wordle-ai](https://github.com/djlynn03/wordle-ai)
