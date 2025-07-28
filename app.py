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
    "Bacterial_spot": "🔴 **Bệnh đốm vi khuẩn**\nNguyên nhân: Vi khuẩn Xanthomonas.\nTriệu chứng: Đốm nhỏ đen/nâu, lá rách.\nTác hại: Giảm quang hợp, ảnh hưởng phát triển.",
    "Late_blight": "🔵 **Mốc sương muộn**\nNguyên nhân: Nấm Phytophthora.\nTriệu chứng: Mảng nâu đậm, viền vàng.\nTác hại: Gây héo, chết cây hàng loạt.",
    "Leaf_Mold": "🟡 **Mốc lá**\nNguyên nhân: Nấm Cladosporium.\nTriệu chứng: Đốm vàng, mốc xám.\nTác hại: Rụng lá sớm, giảm năng suất.",
    "Septoria_leaf_spot": "🟠 **Đốm lá Septoria**\nNguyên nhân: Nấm Septoria.\nTriệu chứng: Đốm tròn, viền sẫm.\nTác hại: Rụng lá, cây yếu.",
    "Yellow_Leaf_Curl_Virus": "🟣 **Bệnh xoăn vàng lá**\nNguyên nhân: Virus TYLCV qua bọ phấn trắng.\nTriệu chứng: Lá xoăn, vàng, cây kém phát triển.\nTác hại: Giảm năng suất nặng nề.",
    "healthy": "✅ **Lá khỏe mạnh**\nKhông có dấu hiệu bệnh lý. Màu xanh đều, không xoăn hay đốm."
}

# --- Cấu hình trang và CSS tùy chỉnh để làm đẹp giao diện ---
st.set_page_config(page_title="Ứng dụng Nhận diện Bệnh Lá Cà Chua", page_icon="�", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700;900&display=swap');

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
        color: #B22222;
        text-align: center;
        margin-bottom: 1rem;
        font-size: 3em;
        font-weight: 700;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* === CSS CHO NHÃN TÙY CHỈNH CỦA KHUNG TẢI LÊN === */
    .upload-label {
        font-size: 24px !important;
        font-weight: 900 !important;
        color: #c62828 !important;
        text-align: center !important;
        line-height: 1.4 !important;
        display: block;
        margin-bottom: 10px; /* Thêm khoảng cách với khung bên dưới */
    }
    /* === KẾT THÚC CSS CẬP NHẬT === */

    .centered-text {
        text-align: center;
        font-size: 1.2em;
        margin-bottom: 1.5rem;
    }
    .stFileUploader {
        border: 2px dashed #a7d9b5;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        background-color: #e6ffe6;
        transition: all 0.3s ease-in-out;
    }
    .stFileUploader:hover {
        border-color: #28a745;
        background-color: #d4ffd4;
    }
    .stFileUploader > div > button {
        background-color: #28a745;
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
        color: #28a745 !important;
    }
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 5px;
        padding: 10px;
        margin-top: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        font-size: 1.1em;
    }
    .stSuccess {
        background-color: #d4edda;
        color: #155724;
        border-left: 5px solid #28a745;
        font-weight: bold;
    }
    .stInfo {
        background-color: #d1ecf1;
        color: #0c5460;
        border-left: 5px solid #17a2b8;
    }
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
</style>
""", unsafe_allow_html=True)

# --- Giao diện Streamlit ---
st.title("🍅 ỨNG DỤNG NHẬN DIỆN BỆNH QUA LÁ CÀ CHUA 🍃")

# Sử dụng markdown để tạo nhãn tùy chỉnh, to, đậm và nổi bật
st.markdown('<p class="upload-label">👇 Bấm vào đây để chụp hoặc tải ảnh lá cà chua lên</p>', unsafe_allow_html=True)

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

        st.success(f"✅ Phát hiện: **{formatted_ten_benh}** (Độ tin cậy: {do_tin_cay:.1f}%)")

        # Hiển thị mô tả bệnh
        st.info(f"💡 **Thông tin bệnh:** {mo_ta_benh.get(ten_benh_goc, 'Không có mô tả chi tiết cho loại bệnh này.')}")
    else:
        st.warning("🥺 Không phát hiện được bệnh nào. Vui lòng thử ảnh khác hoặc đảm bảo ảnh rõ ràng.")

# Thêm footer
st.markdown("---")
st.markdown('<div class="footer">Dự án được thực hiện bởi nhóm nghiên cứu AI.</div>', unsafe_allow_html=True)
