import streamlit as st
import requests
from PIL import Image
import io
import base64
import os
from dotenv import load_dotenv # Import thư viện dotenv

# --- Tải biến môi trường từ file .env ---
# Chỉ dùng khi chạy cục bộ. Khi triển khai lên Streamlit Cloud,
# API Key sẽ được lấy từ Streamlit Secrets.
load_dotenv()

# --- Cấu hình mô hình Roboflow ---
# LƯU Ý QUAN TRỌNG: ROBOFLOW_API_KEY được lấy từ biến môi trường (từ file .env khi chạy cục bộ,
# hoặc từ Streamlit Secrets khi triển khai lên Streamlit Cloud).
# Bạn đã cung cấp API Key: rSUzaeMGYrBA449orJYK
KHOA_API = os.getenv("ROBOFLOW_API_KEY")

TEN_MO_HINH = "tomato-leaf-diseases-lmem9"
PHIEN_BAN = "1"
DIA_CHI_API = f"https://detect.roboflow.com/{TEN_MO_HINH}/{PHIEN_BAN}?api_key={KHOA_API}"

# --- Hàm xử lý ảnh và gửi đến Roboflow ---
def du_doan_benh(anh):
    """Gửi ảnh đến API Roboflow để nhận dạng."""
    bo_dem = io.BytesIO()
    anh.save(bo_dem, quality=90, format="JPEG")
    anh_mahoa = base64.b64encode(bo_dem.getvalue()).decode("utf-8")
    phan_hoi = requests.post(DIA_CHI_API, data=anh_mahoa, headers={"Content-Type": "application/x-www-form-urlencoded"})
    return phan_hoi.json()

# --- Thông tin mô tả bệnh ---
mo_ta_benh = {
    "Bacterial_spot": "🔴 **Bệnh đốm vi khuẩn**\n* **Nguyên nhân:** Vi khuẩn Xanthomonas.\n* **Triệu chứng:** Đốm nhỏ đen/nâu, lá rách.\n* **Tác hại:** Giảm quang hợp, ảnh hưởng phát triển.",
    "Late_blight": "🔵 **Mốc sương muộn**\n* **Nguyên nhân:** Nấm Phytophthora.\n* **Triệu chứng:** Mảng nâu đậm, viền vàng.\n* **Tác hại:** Gây héo, chết cây hàng loạt.",
    "Leaf_Mold": "🟡 **Mốc lá**\n* **Nguyên nhân:** Nấm Cladosporium.\n* **Triệu chứng:** Đốm vàng, mốc xám.\n* **Tác hại:** Rụng lá sớm, giảm năng suất.",
    "Septoria_leaf_spot": "🟠 **Đốm lá Septoria**\n* **Nguyên nhân:** Nấm Septoria.\n* **Triệu chứng:** Đốm tròn, viền sẫm.\n* **Tác hại:** Rụng lá, cây yếu.",
    "Yellow_Leaf_Curl_Virus": "🟣 **Bệnh xoăn vàng lá**\n* **Nguyên nhân:** Virus TYLCV qua bọ phấn trắng.\n* **Triệu chứng:** Lá xoăn, vàng, cây kém phát triển.\n* **Tác hại:** Giảm năng suất nặng nề.",
    "healthy": "✅ **Lá khỏe mạnh**\nKhông có dấu hiệu bệnh lý. Cây phát triển tốt, lá có màu xanh đều, không có biểu hiện xoăn hay đốm bất thường."
}

# --- Cấu hình trang và CSS tùy chỉnh để làm đẹp giao diện ---
st.set_page_config(page_title="Ứng dụng Nhận diện Bệnh Lá Cà Chua", page_icon="🍅", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
        color: #333;
        font-size: 1.1em;
    }
    .stApp {
        background-color: #f0f2f6;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 700px;
        margin: auto;
    }
    h1 {
        color: #B22222; /* Màu đỏ nổi bật hơn (FireBrick) */
        text-align: center;
        margin-bottom: 1rem;
        font-size: 3em;
        font-weight: 700;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    .centered-text {
        text-align: center;
        font-size: 1.2em;
        margin-bottom: 1.5rem;
    }
    
    /* CSS cho st.file_uploader */
    .stFileUploader {
        border: 2px dashed #a7d9b5;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        background-color: #e6ffe6;
        transition: all 0.3s ease-in-out;
        min-height: 150px; /* Đảm bảo đủ không gian cho văn bản */
        display: flex; /* Sử dụng flexbox để căn giữa nội dung */
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative; /* Cần thiết cho các pseudo-element */
    }
    .stFileUploader:hover {
        border-color: #28a745;
        background-color: #d4ffd4;
    }

    /* Ẩn văn bản "Drag and drop file here" và "Limit 200MB per file..." */
    .stFileUploader [data-testid="stFileUploaderDropzone"] p {
        display: none !important;
    }

    /* Ẩn văn bản "Browse files" mặc định */
    .stFileUploader [data-testid="stFileUploaderDropzone"] button span {
        visibility: hidden; /* Ẩn văn bản gốc */
        position: relative;
    }

    /* Chèn văn bản "Duyệt tệp" vào nút */
    .stFileUploader [data-testid="stFileUploaderDropzone"] button::after {
        content: ""; /* Đã thay đổi thành rỗng để ẩn văn bản "Duyệt tệp" */
        visibility: visible;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: white;
        font-weight: bold;
        font-size: 1em;
        z-index: 2; /* Đảm bảo nằm trên nút */
    }

    .stFileUploader > div > button {
        background-color: #28a745;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: background-color 0.3s ease;
        position: relative; /* Để ::after có thể định vị */
        overflow: hidden; /* Đảm bảo text không tràn ra ngoài */
        margin-top: 20px; /* Khoảng cách với label */
        z-index: 2; /* Đảm bảo nút nằm trên các pseudo-element khác */
    }
    .stFileUploader > div > button:hover {
        background-color: #218838;
    }
    .stImage {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stSpinner > div > div {
        color: #28a745 !important;
    }

    /* === CSS ĐÃ CẬP NHẬT ĐỂ LÀM NỔI BẬT KẾT QUẢ === */
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 8px;
        padding: 18px;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.08);
        font-size: 1.4em !important; /* Tăng kích thước chữ của kết quả */
        line-height: 1.6;
    }
    .stSuccess {
        background-color: #d4edda;
        color: #155724;
        border-left: 6px solid #28a745;
        font-weight: 700 !important; /* Làm chữ đậm hơn */
    }
    .stInfo {
        background-color: #d1ecf1;
        color: #0c5460;
        border-left: 6px solid #17a2b8;
        font-weight: 500 !important; /* Cũng làm chữ đậm hơn */
    }
    /* === KẾT THÚC CSS CẬP NHẬT === */

    .stWarning {
        background-color: #fff3cd;
        color: #856404;
        border-left: 5px solid #ffc107;
    }
    .stError {
        background-color: #f8d7da;
        color: #721c24;
        border-left: 5px solid #dc3545;
    }
    .footer {
        text-align: center;
        margin-top: 30px;
        padding-top: 15px;
        border-top: 1px solid #eee;
        color: #777;
        font-size: 0.9em;
    }

    /* Đã loại bỏ CSS để đặt icon bàn tay dưới dòng chữ chính trong label */
    /* .stFileUploader label::after {
        content: "👇";
        display: block;
        font-size: 1.5em;
        margin-top: 5px;
    } */
</style>
""", unsafe_allow_html=True)

# --- Giao diện Streamlit ---
st.title("🍅 ỨNG DỤNG NHẬN DIỆN BỆNH QUA LÁ CÀ CHUA 🍃")

# Sử dụng markdown để tạo nhãn tùy chỉnh, to, đậm và nổi bật
st.markdown('<p class="upload-label">Bấm vào đây để chụp hoặc tải ảnh lá cà chua lên</p>', unsafe_allow_html=True)
# Thêm icon bàn tay 👇 ở dòng riêng, căn giữa và bên dưới dòng chữ trên
st.markdown('<p style="text-align: center; font-size: 1.5em; margin-top: -10px; margin-bottom: 10px;">👇</p>', unsafe_allow_html=True)


# Ẩn nhãn mặc định của file_uploader và sử dụng nhãn tùy chỉnh ở trên
tep_anh = st.file_uploader(
    label="Tải ảnh lên", # Dòng chữ này sẽ không hiển thị
    type=["jpg", "jpeg", "png"],
    help="Hỗ trợ các định dạng: JPG, JPEG, PNG. Dung lượng tối đa 200MB.",
    label_visibility="collapsed" # Thuộc tính quan trọng để ẩn nhãn mặc định
)


if tep_anh is not None:
    anh = Image.open(tep_anh).convert("RGB")
    st.image(anh, caption="📷 Ảnh đã tải lên", use_container_width=True)

    with st.spinner("🔍 Đang phân tích... Vui lòng chờ ⏳"):
        ket_qua = du_doan_benh(anh)

    du_doan = ket_qua.get("predictions", [])
    if du_doan:
        benh = du_doan[0]
        ten_benh_goc = benh["class"]
        do_tin_cay = round(benh["confidence"] * 100, 2)

        # Định dạng tên bệnh để hiển thị đẹp hơn
        formatted_ten_benh = ' '.join([word.capitalize() for word in ten_benh_goc.split('_')])

        st.success(f"**Phát hiện:** {formatted_ten_benh} (Độ tin cậy: {do_tin_cay:.1f}%)")

        # Hiển thị mô tả bệnh
        st.info(f"**Thông tin bệnh:**\n{mo_ta_benh.get(ten_benh_goc, 'Không có mô tả chi tiết cho loại bệnh này.')}")
    else:
        st.warning("🥺 Không phát hiện được bệnh nào. Vui lòng thử ảnh khác hoặc đảm bảo ảnh rõ ràng.")

# Thêm footer
st.markdown("---")
st.markdown('<div class="footer">Dự án được thực hiện bởi nhóm nghiên cứu AI.</div>', unsafe_allow_html=True)
