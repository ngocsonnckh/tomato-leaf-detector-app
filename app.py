import streamlit as st
import requests
from PIL import Image
import io
import base64
import os
from dotenv import load_dotenv # Import thư viện dotenv
import streamlit.components.v1 as components # Import components để nhúng HTML/JS

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
    /* CSS cho custom uploader */
    .custom-uploader-container {
        border: 2px dashed #a7d9b5;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        background-color: #e6ffe6;
        transition: all 0.3s ease-in-out;
        cursor: pointer;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 150px; /* Chiều cao tối thiểu */
        position: relative;
        overflow: hidden; /* Để ẩn input file gốc */
    }
    .custom-uploader-container:hover {
        border-color: #28a745;
        background-color: #d4ffd4;
    }
    .custom-uploader-container input[type="file"] {
        position: absolute;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        opacity: 0; /* Ẩn input file gốc */
        cursor: pointer;
    }
    .custom-uploader-text-main {
        font-weight: bold;
        font-size: 1.2em;
        color: #333;
        margin-bottom: 5px;
    }
    .custom-uploader-text-limit {
        font-size: 0.9em;
        color: #555;
        margin-top: 5px;
    }
    .custom-uploader-button {
        background-color: #28a745;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: background-color 0.3s ease;
        margin-top: 15px; /* Khoảng cách với text */
        display: inline-block; /* Để nút không chiếm hết chiều rộng */
    }
    .custom-uploader-button:hover {
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
</style>
""", unsafe_allow_html=True)

# --- Giao diện Streamlit ---
st.title("🍅 ỨNG DỤNG NHẬN DIỆN BỆNH QUA LÁ CÀ CHUA 🍃")
st.markdown('<p class="centered-text">Vui lòng chụp hoặc tải lên ảnh lá cà chua (có thể là lá khỏe hoặc bị bệnh) 🌱</p>', unsafe_allow_html=True)

# --- Thành phần tải ảnh lên tùy chỉnh bằng HTML/JavaScript ---
# Đây là phần thay thế cho st.file_uploader mặc định
custom_uploader_html = """
<div class="custom-uploader-container" id="customUploader">
    <input type="file" id="fileInput" accept="image/jpeg, image/png, image/jpg">
    <div class="custom-uploader-text-main">Kéo và thả tệp vào đây</div>
    <div class="custom-uploader-text-limit">Giới hạn 200MB mỗi tệp (JPG, JPEG, PNG)</div>
    <div class="custom-uploader-button">Duyệt tệp</div>
    <div id="fileNameDisplay" style="margin-top: 10px; font-size: 0.9em; color: #666;"></div>
</div>

<script>
    const fileInput = document.getElementById('fileInput');
    const customUploader = document.getElementById('customUploader');
    const fileNameDisplay = document.getElementById('fileNameDisplay');
    const componentKey = "custom_uploader_component"; // Key của component Streamlit

    // Hàm để gửi dữ liệu về Streamlit
    function sendDataToStreamlit(dataPayload) {
        if (window.Streamlit && window.Streamlit.setComponentValue) {
            window.Streamlit.setComponentValue(dataPayload);
        } else {
            console.error("Streamlit object or setComponentValue not found. Cannot send data.");
        }
    }

    // Gửi giá trị null ban đầu khi component được tải để Streamlit nhận biết
    // và tránh lỗi TypeError khi uploaded_image_data chưa có giá trị.
    // Đảm bảo Streamlit đã sẵn sàng trước khi gửi.
    document.addEventListener('DOMContentLoaded', function() {
        if (window.Streamlit && window.Streamlit.setComponentValue) {
            sendDataToStreamlit(null); // Gửi null để khởi tạo
        }
    });

    fileInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                sendDataToStreamlit({
                    data: e.target.result, // Base64 encoded image
                    name: file.name,
                    type: file.type
                });
                fileNameDisplay.textContent = `Đã chọn: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
            };
            reader.readAsDataURL(file);
        } else {
            sendDataToStreamlit(null); // Gửi null khi không có file
            fileNameDisplay.textContent = '';
        }
    });

    // Handle drag and drop
    customUploader.addEventListener('dragover', (e) => {
        e.preventDefault();
        customUploader.style.borderColor = '#28a745';
        customUploader.style.backgroundColor = '#d4ffd4';
    });

    customUploader.addEventListener('dragleave', () => {
        customUploader.style.borderColor = '#a7d9b5';
        customUploader.style.backgroundColor = '#e6ffe6';
    });

    customUploader.addEventListener('drop', (e) => {
        e.preventDefault();
        customUploader.style.borderColor = '#a7d9b5';
        customUploader.style.backgroundColor = '#e6ffe6';
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files; // Assign dropped files to the input
            fileInput.dispatchEvent(new Event('change')); // Trigger change event
        }
    });
</script>
"""
# Nhúng thành phần tùy chỉnh vào Streamlit
uploaded_image_data = components.html(
    custom_uploader_html,
    height=200, # Chiều cao của thành phần tùy chỉnh
    scrolling=False,
    key="custom_uploader_component" # Key duy nhất cho thành phần
)

# Xử lý dữ liệu ảnh được gửi từ JavaScript
tep_anh = None
# Kiểm tra nếu uploaded_image_data không phải là None và có chứa 'data'
# Thêm kiểm tra uploaded_image_data có phải là dict không trước khi truy cập .get()
if uploaded_image_data and isinstance(uploaded_image_data, dict) and uploaded_image_data.get('data'):
    # Chuyển đổi base64 data URL thành bytes
    base64_string = uploaded_image_data['data'].split(',')[1]
    image_bytes = base64.b64decode(base64_string)
    
    # Tạo đối tượng BytesIO để Streamlit.Image.open có thể đọc
    tep_anh = io.BytesIO(image_bytes)
    tep_anh.name = uploaded_image_data.get('name', 'uploaded_image.png') # Gán lại tên file

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
