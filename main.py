import streamlit as st
from PIL import Image
import numpy as np
from collections import Counter

def get_hex_color_codes(image, num_colors=20):
    # Resmi numpy dizisine dönüştür ve renkleri çıkar
    image = np.array(image)
    pixels = image.reshape(-1, 3)

    # En yaygın renkleri say
    colors = Counter(map(tuple, pixels))
    most_common_colors = colors.most_common(num_colors)

    # Renkleri HEX kodlarına dönüştür ve yüzdelerini hesapla
    total_pixels = len(pixels)
    hex_colors = [(color, count / total_pixels * 100) for color, count in most_common_colors]
    return hex_colors

def display_color(hex_color, percentage):
    # Renk kutusunu ve yüzdesini göster
    st.markdown(
        f"<div style='display: inline-block; margin: 10px; padding: 10px; background-color: {hex_color}; color: white; border-radius: 5px;'>{hex_color} - {percentage:.2f}%</div>", 
        unsafe_allow_html=True)

def main():
    st.title("Resimden Hex Renk Kodu Çıkarıcı")
    uploaded_file = st.file_uploader("Bir resim dosyası yükle (PNG, JPEG, JPG)", type=["png", "jpeg", "jpg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert('RGB')
        hex_codes = get_hex_color_codes(image)
        st.write("En Sık Bulunan 20 Hex Renk Kodu ve Yüzdelikleri:")
        for hex_color, percentage in hex_codes:
            display_color(hex_color, percentage)
        st.image(image, caption='Yüklenen Resim', use_column_width=True)

if __name__ == "__main__":
    main()

