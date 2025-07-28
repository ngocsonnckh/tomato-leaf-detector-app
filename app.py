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
    bo_dem = io.BytesIO()
    anh.save(bo_dem, quality=90, format="JPEG")
    anh_mahoa = base64.b64encode(bo_dem.getvalue()).decode("utf-8")
    phan_hoi = requests.post(DIA_CHI_API, data=anh_mahoa, headers={"Content-Type": "application/x-www-form-urlencoded"})
    return phan_hoi.json()

# --- Thông tin mô tả bệnh ---
mo_ta_benh = {
    "Bacterial_spot": "🔴 **Bệnh đốm vi khuẩn**\nNguyên nhân: Vi khuẩn Xanthomonas.\nTriệu chứng: Đốm nhỏ đen/nâu, lá rách.\nTác hại: Giảm quang hợp, ảnh hưởng phát triển.",
    "Late_blight": "🔵 **Mốc sương muộn**\nNguyên nhân: Nấm Phytophthora.\nTriệu chứng: Mảng nâu đậm, viền vàng.\nTác hại: Gây héo, chết cây hàng loạt.",
    "Leaf_Mold": "🟡 **Mốc lá**\nNguyên nhân: Nấm Cladosporium.\nTriệu chứng: Đốm vàng, mốc xám.\nTác hại: Rụng lá sớm, giảm năng suất.",
    "Septoria_leaf_spot": "🟠 **Đốm lá Septoria**\nNguyên nhân: Nấm Septoria.\nTriệu chứng: Đốm tròn, viền sẫm.\nTác hại: Rụng lá, cây yếu.",
    "Yellow_Leaf_Curl_Virus": "🟣 **Bệnh xoăn vàng lá**\nNguyên nhân: Virus TYLCV qua bọ phấn trắng.\nTriệu chứng: Lá xoăn, vàng, cây kém phát triển.\nTác hại: Giảm năng suất nặng nề.",
    "healthy": "✅ **Lá khỏe mạnh**\nKhông có dấu hiệu bệnh lý. Màu xanh đều, không xoăn hay đốm."
}

# --- Cấu hình trang và CSS tùy chỉnh để làm đẹp giao diện ---
st.set_page_config(page_title="Ứng dụng Nhận diện Bệnh Lá Cà Chua", page_icon="🍅", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
        color: #333;
        font-size: 1.1em; /* Tăng kích thước font chữ cơ bản */
    }
    .stApp {
        background-color: #f0f2f6; /* Màu nền nhẹ nhàng */
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 700px; /* Giới hạn chiều rộng nội dung */
        margin: auto;
    }
    h1 {
        color: #B22222; /* Màu đỏ nổi bật hơn (FireBrick) */
        text-align: center;
        margin-bottom: 1rem;
        font-size: 3em; /* Tăng kích thước tiêu đề lớn hơn */
        font-weight: 700; /* Đảm bảo độ đậm */
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .centered-text { /* CSS mới để căn giữa văn bản */
        text-align: center;
        font-size: 1.2em; /* Tăng kích thước chữ cho mô tả */
        margin-bottom: 1.5rem; /* Khoảng cách dưới */
    }
    .stFileUploader {
        border: 2px dashed #a7d9b5; /* Viền nét đứt màu xanh */
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        background-color: #e6ffe6; /* Nền xanh nhạt */
        transition: all 0.3s ease-in-out;
    }
    .stFileUploader:hover {
        border-color: #28a745;
        background-color: #d4ffd4;
    }
    .stFileUploader > div > button {
        background-color: #28a745; /* Nút Browse files */
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    .stFileUploader > div > button:hover {
        background-color: #218838;
    }
    .stImage {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stSpinner > div > div {
        color: #28a745 !important; /* Màu spinner */
    }
    .stSuccess {
        background-color: #d4edda;
        color: #155724;
        border-left: 5px solid #28a745;
        border-radius: 5px;
        padding: 10px;
        margin-top: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        font-size: 1.1em; /* Tăng kích thước font */
        font-weight: bold; /* Đảm bảo đậm */
    }
    .stInfo {
        background-color: #d1ecf1;
        color: #0c5460;
        border-left: 5px solid #17a2b8;
        border-radius: 5px;
        padding: 10px;
        margin-top: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        font-size: 1.1em; /* Tăng kích thước font */
    }
    .stWarning {
        background-color: #fff3cd;
        color: #856404;
        border-left: 5px solid #ffc107;
        border-radius: 5px;
        padding: 10px;
        margin-top: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        font-size: 1.1em; /* Tăng kích thước font */
    }
    .stError {
        background-color: #f8d7da;
        color: #721c24;
        border-left: 5px solid #dc3545;
        border-radius: 5px;
        padding: 10px;
        margin-top: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        font-size: 1.1em; /* Tăng kích thước font */
    }
    .footer {
        text-align: center;
        margin-top: 30px;
        padding-top: 15px;
        border-top: 1px solid #eee;
        color: #777;
        font-size: 0.9em;
    }

    /* CSS để ẩn văn bản tiếng Anh mặc định và thay thế bằng tiếng Việt */
    /* Target the "Drag and drop file here" text inside the uploader */
    .stFileUploader [data-testid="stFileUploaderDropzone"] p:first-child {
        display: none !important; /* Ẩn văn bản gốc hoàn toàn */
    }
    .stFileUploader [data-testid="stFileUploaderDropzone"] > div:first-child::before { /* Target div chứa p tag */
        content: "Kéo và thả tệp vào đây"; /* Chèn văn bản tiếng Việt */
        display: block;
        text-align: center;
        color: #333; /* Đảm bảo dễ đọc */
        font-weight: bold; /* In đậm */
        font-size: 1.2em; /* Kích thước phù hợp */
        margin-bottom: 5px; /* Khoảng cách dưới */
    }

    /* Target the "Limit 200MB per file • JPG, JPEG, PNG" text */
    .stFileUploader [data-testid="stFileUploaderDropzone"] p:last-child {
        display: none !important; /* Ẩn văn bản gốc hoàn toàn */
    }
    .stFileUploader [data-testid="stFileUploaderDropzone"] > div:first-child::after { /* Target div chứa p tag */
        content: "Giới hạn 200MB mỗi tệp (JPG, JPEG, PNG)"; /* Chèn văn bản tiếng Việt */
        display: block;
        text-align: center;
        color: #555; /* Đảm bảo dễ đọc */
        font-size: 0.9em; /* Kích thước phù hợp */
        margin-top: 5px; /* Khoảng cách trên */
    }

    /* Target the "Browse files" button text */
    .stFileUploader [data-testid="stFileUploaderDropzone"] button span {
        display: none !important; /* Ẩn văn bản gốc */
    }
    .stFileUploader [data-testid="stFileUploaderDropzone"] button::after {
        content: "Duyệt tệp"; /* Chèn văn bản tiếng Việt */
        color: white;
        font-weight: bold;
        font-size: 1em; /* Kích thước phù hợp */
    }
</style>
""", unsafe_allow_html=True)

# --- Giao diện Streamlit ---
st.title("🍅 ỨNG DỤNG NHẬN DIỆN BỆNH QUA LÁ CÀ CHUA 🍃")
st.markdown('<p class="centered-text">Vui lòng chụp hoặc tải lên ảnh lá cà chua (có thể là lá khỏe hoặc bị bệnh) 🌱</p>', unsafe_allow_html=True)

tep_anh = st.file_uploader(
    "Kéo và thả tệp vào đây hoặc nhấp để duyệt", # Tham số này không còn hiển thị trực tiếp do CSS tùy chỉnh
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed", # Ẩn nhãn mặc định để phù hợp với giao diện ảnh mẫu
    help="Giới hạn 200MB mỗi tệp" # Tham số này không còn hiển thị trực tiếp do CSS tùy chỉnh
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

        # Định dạng tên bệnh để hiển thị đẹp hơn (ví dụ: "Bacterial_spot" -> "Bacterial Spot")
        formatted_ten_benh = ' '.join([word.capitalize() for word in ten_benh_goc.split('_')])

        st.success(f"✅ Phát hiện: **{formatted_ten_benh}** (Độ tin cậy: {do_tin_cay:.1f}%)")

        # Hiển thị mô tả bệnh
        st.info(f"💡 **Thông tin bệnh:** {mo_ta_benh.get(ten_benh_goc, 'Không có mô tả chi tiết cho loại bệnh này.')}")
    else:
        st.warning("🥺 Không phát hiện bệnh nào. Vui lòng thử ảnh khác hoặc đảm bảo ảnh rõ ràng.")

# Thêm một số khoảng trống và footer cuối cùng
st.markdown("---")
st.markdown('<div class="footer">Dự án được thực hiện bởi nhóm nghiên cứu AI.</div>', unsafe_allow_html=True)
