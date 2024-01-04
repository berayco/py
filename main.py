import streamlit as st
import cv2
from PIL import Image
import numpy as np
from collections import Counter

def get_hex_color_codes(image):
    # Resmi RGB'ye dönüştür
    image = np.array(image.convert('RGB'))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Resmi yeniden boyutlandırarak renkleri daha iyi algılamaya çalış
    resized_image = cv2.resize(image, (40, 40), interpolation=cv2.INTER_AREA)
    pil_image = Image.fromarray(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB))

    # 'P' moduna dönüştür
    pil_image = pil_image.convert('P', palette=Image.ADAPTIVE, colors=256)

    # Renkleri al ve bir Counter oluştur
    colors = pil_image.getcolors(20*20) or []
    if not colors:
        return []  # Eğer renk bulunamazsa boş liste döndür

    total_pixels = sum(count for color, count in colors)
    color_counts = Counter({'#{:02x}{:02x}{:02x}'.format(*color): count for color, count in colors if isinstance(color, tuple) and len(color) == 3})
    most_common_colors = color_counts.most_common(20)
    return [(color, count / total_pixels * 100) for color, count in most_common_colors]

def display_color(hex_color, percentage):
    st.markdown(
        f"<div style='display: inline-block; margin: 10px; padding: 10px; background-color: {hex_color}; color: white; border-radius: 5px;'>{hex_color} - {percentage:.2f}%</div>", 
        unsafe_allow_html=True)

def main():
    st.title("Resimden Hex Renk Kodu Çıkarıcı")
    uploaded_file = st.file_uploader("Bir resim dosyası yükle (PNG, JPEG, JPG)", type=["png", "jpeg", "jpg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        hex_codes = get_hex_color_codes(image)
        if hex_codes:
            st.write("En Sık Bulunan 20 Hex Renk Kodu ve Yüzdelikleri:")
            for hex_color, percentage in hex_codes:
                display_color(hex_color, percentage)
        else:
            st.write("Bu resimde yeterli renk çeşitliliği bulunamadı.")
        st.image(image, caption='Yüklenen Resim', use_column_width=True)

if __name__ == "__main__":
    main()

