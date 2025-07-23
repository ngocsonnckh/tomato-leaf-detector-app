
# 🍅 Tomato Leaf Disease Detector

Ứng dụng sử dụng mô hình AI để nhận diện các bệnh phổ biến trên lá cà chua qua hình ảnh, được huấn luyện trên nền tảng Roboflow.

## 🚀 Cách sử dụng

1. **Clone hoặc tải repository về máy**:
    ```bash
    git clone https://github.com/ngocsonnckh/tomato-leaf-detector-app.git
    ```

2. **Cài đặt thư viện cần thiết**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Tạo file `.env` chứa Roboflow API key**:
    - Tạo file `.env` (hoặc copy từ `env.example`) và điền:
    ```env
    ROBOFLOW_API_KEY=your_api_key_here
    ```

4. **Chạy ứng dụng**:
    ```bash
    streamlit run app.py
    ```

## 📂 Các tệp chính

- `app.py`: File chạy ứng dụng Streamlit.
- `requirements.txt`: Danh sách thư viện cần cài.
- `env.example`: Mẫu file `.env` (không chứa API thật).
- `.gitignore`: Bỏ qua file `.env` khi đẩy lên GitHub.
- `README.md`: Tài liệu hướng dẫn sử dụng.

## 📝 Mô tả mô hình

Mô hình được huấn luyện trên Roboflow, phát hiện các loại bệnh:
- Bacterial Spot
- Late Blight
- Leaf Mold
- Septoria Leaf Spot
- Yellow Leaf Curl Virus
- Healthy

## 🔒 Lưu ý bảo mật

**Không đưa trực tiếp API key vào mã nguồn.** Sử dụng file `.env` và thêm `.env` vào `.gitignore` để đảm bảo an toàn.

---

© 2025 – tomato-leaf-detector-app | NgocSonNCKH
