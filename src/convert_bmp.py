
import os
from PIL import Image

# Proje ana dizinini temel alan dosya yolları
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(BASE_DIR, 'input')
OUTPUT_DIR = os.path.join(BASE_DIR, 'generated_bmp')

# Giriş resmi
SOURCE_IMAGE_PATH = os.path.join(INPUT_DIR, 'resim.png')


def convert_to_bw(source_path, dest_path):
    """
    Görüntüyü 1-bit siyah-beyaz BMP formatına dönüştürür.
    """
    try:
        with Image.open(source_path) as img:
            # '1' modu 1-bit pikseller, siyah-beyaz
            bw_img = img.convert('1')
            bw_img.save(dest_path, 'bmp')
            print(f"'{dest_path}' olarak 1-bit siyah-beyaz BMP oluşturuldu.")
    except FileNotFoundError:
        print(f"Hata: '{source_path}' bulunamadı. Lütfen 'input' klasörüne 'resim.png' dosyasını ekleyin.")
    except Exception as e:
        print(f"1-bit BMP oluşturulurken bir hata oluştu: {e}")


def convert_to_4bit_grayscale(source_path, dest_path):
    """
    Görüntüyü 4-bit (16 seviye) gri tonlamalı BMP formatına dönüştürür.
    Pillow doğrudan 4-bit kaydetmeyi desteklemediği için paletli mod kullanılır.
    """
    try:
        with Image.open(source_path) as img:
            # Görüntüyü 8-bit grayscale'e çevir
            gray_img = img.convert('L')
            # 16 renkli bir paletle (4-bit) yeni bir paletli görüntü oluştur
            # Bu, görüntüyü 16 gri seviyesine indirger.
            quantized_img = gray_img.quantize(colors=16)
            quantized_img.save(dest_path, 'bmp')
            print(f"'{dest_path}' olarak 4-bit gri tonlamalı BMP oluşturuldu.")
    except FileNotFoundError:
        print(f"Hata: '{source_path}' bulunamadı.")
    except Exception as e:
        print(f"4-bit BMP oluşturulurken bir hata oluştu: {e}")


def convert_to_8bit_color(source_path, dest_path):
    """
    Görüntüyü 8-bit (256 renk) paletli BMP formatına dönüştürür.
    """
    try:
        with Image.open(source_path) as img:
            # Görüntüyü 256 renkli palete indirge
            # 'P' modu paletli görüntü anlamına gelir
            color_img = img.quantize(colors=256)
            color_img.save(dest_path, 'bmp')
            print(f"'{dest_path}' olarak 8-bit renkli BMP oluşturuldu.")
    except FileNotFoundError:
        print(f"Hata: '{source_path}' bulunamadı.")
    except Exception as e:
        print(f"8-bit BMP oluşturulurken bir hata oluştu: {e}")


def main():
    """
    Ana fonksiyon, tüm dönüştürme işlemlerini başlatır.
    """
    # Çıktı klasörünün var olduğundan emin ol
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Hedef dosya yolları
    dest_bw_path = os.path.join(OUTPUT_DIR, 'black_and_white.bmp')
    dest_gray4_path = os.path.join(OUTPUT_DIR, '4bit_grayscale.bmp')
    dest_color8_path = os.path.join(OUTPUT_DIR, 'color_table.bmp')

    # Dönüştürme fonksiyonlarını çağır
    convert_to_bw(SOURCE_IMAGE_PATH, dest_bw_path)
    convert_to_4bit_grayscale(SOURCE_IMAGE_PATH, dest_gray4_path)
    convert_to_8bit_color(SOURCE_IMAGE_PATH, dest_color8_path)


if __name__ == '__main__':
    main()
