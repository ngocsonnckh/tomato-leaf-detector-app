
import streamlit as st
import requests
from PIL import Image
import io
import base64

# --- Cấu hình mô hình Roboflow ---
KHOA_API = "rSUzaeMGYrBA449orJYK"  # Ẩn thông tin API Key nếu chia sẻ công khai
TEN_MO_HINH = "tomato-leaf-diseases-lmem9"
PHIEN_BAN = "1"
DIA_CHI_API = f"https://detect.roboflow.com/{TEN_MO_HINH}/{PHIEN_BAN}?api_key={KHOA_API}"

# --- CSS tuỳ chỉnh cho giao diện ---
st.markdown("""
    <style>
        .main {
            background-color: #f9f9f9;
            font-family: 'Segoe UI', sans-serif;
        }
        .title {
            color: #D7263D;
            text-align: center;
            font-size: 32px;
            font-weight: bold;
        }
        .subtitle {
            color: #3F88C5;
            font-size: 18px;
            margin-bottom: 20px;
        }
        .stButton>button {
            background-color: #3F88C5;
            color: white;
            border-radius: 8px;
            padding: 10px 16px;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #265D8E;
        }
    </style>
""", unsafe_allow_html=True)

# --- Giao diện Streamlit ---
st.set_page_config(page_title="Nhận diện bệnh lá cà chua", layout="centered")
st.markdown('<div class="title">🍅 ỨNG DỤNG NHẬN DIỆN BỆNH QUA LÁ CÀ CHUA </div>', unsafe_allow_html=True)

st.write("📤 Vui lòng chụp hoặc tải lên ảnh lá cà chua (có thể lá khỏe hoặc bị bệnh)")

tep_anh = st.file_uploader("Chọn ảnh (jpg, jpeg, png)", type=["jpg", "jpeg", "png"])

def du_doan_benh(anh):
    bo_dem = io.BytesIO()
    anh.save(bo_dem, quality=90, format="JPEG")
    anh_mahoa = base64.b64encode(bo_dem.getvalue()).decode("utf-8")
    phan_hoi = requests.post(DIA_CHI_API, data=anh_mahoa, headers={"Content-Type": "application/x-www-form-urlencoded"})
    return phan_hoi.json()

if tep_anh is not None:
    anh = Image.open(tep_anh).convert("RGB")
    st.image(anh, caption="🖼️ Ảnh đã tải lên", use_container_width=True)

    with st.spinner("⏳ Đang phân tích ảnh..."):
        ket_qua = du_doan_benh(anh)

    du_doan = ket_qua.get("predictions", [])
    if du_doan:
        benh = du_doan[0]
        ten_benh = benh["class"]
        do_tin_cay = round(benh["confidence"] * 100, 2)
        st.success(f"✅ Phát hiện: **{{ten_benh}}** (Độ tin cậy: {{do_tin_cay}}%)".format(ten_benh=ten_benh, do_tin_cay=do_tin_cay))

        mo_ta_benh = {
            "Bacterial_spot": "🔴 **Bệnh đốm vi khuẩn**\nNguyên nhân: Vi khuẩn Xanthomonas.\nTriệu chứng: Đốm nhỏ đen/nâu, lá rách.\nTác hại: Giảm quang hợp, ảnh hưởng phát triển.",
            "Late_blight": "🔵 **Mốc sương muộn**\nNguyên nhân: Nấm Phytophthora.\nTriệu chứng: Mảng nâu đậm, viền vàng.\nTác hại: Gây héo, chết cây hàng loạt.",
            "Leaf_Mold": "🟡 **Mốc lá**\nNguyên nhân: Nấm Cladosporium.\nTriệu chứng: Đốm vàng, mốc xám.\nTác hại: Rụng lá sớm, giảm năng suất.",
            "Septoria_leaf_spot": "🟠 **Đốm lá Septoria**\nNguyên nhân: Nấm Septoria.\nTriệu chứng: Đốm tròn, viền sẫm.\nTác hại: Rụng lá, cây yếu.",
            "Yellow_Leaf_Curl_Virus": "🟣 **Bệnh xoăn vàng lá**\nNguyên nhân: Virus TYLCV qua bọ phấn trắng.\nTriệu chứng: Lá xoăn, vàng, cây kém phát triển.\nTác hại: Giảm năng suất nặng nề.",
            "healthy": "✅ **Lá khỏe mạnh**\nKhông có dấu hiệu bệnh lý. Màu xanh đều, không xoăn hay đốm."
        }

        st.info(mo_ta_benh.get(ten_benh, "Không có mô tả chi tiết."))
    else:
        st.warning("⚠️ Không phát hiện bệnh nào.")
   
