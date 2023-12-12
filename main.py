import streamlit as st
import cv2
from PIL import Image
import numpy as np


def get_hex_color_codes(image):
    # Resmi OpenCV formatına dönüştür
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Renk sayısını azaltmak için resmi küçült
    resized_image = cv2.resize(image, (40, 40), interpolation=cv2.INTER_AREA)

    # PIL Image'e dönüştür
    pil_image = Image.fromarray(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB))

    # Baskın renkleri çıkar
    colors = pil_image.getcolors(40*40)
    hex_colors = ['#{:02x}{:02x}{:02x}'.format(*color[1]) for color in colors]

    return hex_colors

# Renk kutusunu gösterme fonksiyonu
def display_color(hex_color):
    # Renk kutusunu ve hex kodunu yan yana göster
    st.markdown(
        f"<div style='display: inline-block; margin: 10px; padding: 10px; background-color: {hex_color}; color: white; border-radius: 5px;'>{hex_color}</div>",
        unsafe_allow_html=True)

# Streamlit uygulamasının ana yapısı
def main():
    st.title("Resimden Hex Renk Kodu Çıkarıcı")

    # Dosya yükleme widget'ı
    uploaded_file = st.file_uploader("Bir PNG dosyası yükle", type=["png"])

    if uploaded_file is not None:
        # PIL ile resmi yükle
        image = Image.open(uploaded_file)

        # Hex renk kodlarını elde et
        hex_codes = get_hex_color_codes(image)

        # Renk kodlarını ve renkleri göster
        st.write("Bulunan Hex Renk Kodları ve Renkler:")
        for hex_color in hex_codes:
            display_color(hex_color)

        # Renkleri görselleştir (opsiyonel)
        st.image(image, caption='Yüklenen Resim', use_column_width=True)

if __name__ == "__main__":
    main()
