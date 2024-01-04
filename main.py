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
    hex_colors = [{'hex': '#{0:02x}{1:02x}{2:02x}'.format(*color), 'percentage': count / total_pixels * 100} for color, count in most_common_colors]
    return hex_colors

def display_colors(hex_colors):
    # Renk kutularını ve yüzdesini göster
    for color in hex_colors:
        st.markdown(
            f"<div style='display: inline-flex; align-items: center; justify-content: center; width: 100px; height: 50px; background-color: {color['hex']}; color: #fff; margin: 10px; border-radius: 10px;'>{color['hex']}<br>({color['percentage']:.2f}%)</div>", 
            unsafe_allow_html=True)

def main():
    st.title("Resimden Hex Renk Kodu Çıkarıcı")
    uploaded_file = st.file_uploader("Bir resim dosyası yükle (PNG, JPEG, JPG)", type=["png", "jpeg", "jpg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert('RGB')
        hex_codes = get_hex_color_codes(image)
        st.write("En Sık Bulunan 20 Hex Renk Kodu:")
        # Renkleri satır satır göster
        col1, col2, col3, col4 = st.columns(4)
        cols = [col1, col2, col3, col4]
        for index, color_info in enumerate(hex_codes):
            with cols[index % 4]:
                display_colors([color_info])
        st.image(image, caption='Yüklenen Resim', use_column_width=True)

if __name__ == "__main__":
    main()
