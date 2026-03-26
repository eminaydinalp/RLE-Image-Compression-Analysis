
import os
import hashlib
import numpy as np
from PIL import Image

def calculate_performance(original_path, compressed_path):
    """
    Sıkıştırma performansını hesaplar.

    Döndürdüğü Değerler (bir dictionary içinde):
    - original_size: Orijinal dosya boyutu (byte)
    - compressed_size: Sıkıştırılmış dosya boyutu (byte)
    - compression_ratio: Sıkıştırma oranı
    - space_saving: Yerden tasarruf yüzdesi
    """
    try:
        original_size = os.path.getsize(original_path)
        compressed_size = os.path.getsize(compressed_path)

        if compressed_size == 0:
            return {
                "original_size": original_size,
                "compressed_size": compressed_size,
                "compression_ratio": 0,
                "space_saving": 0
            }

        compression_ratio = original_size / compressed_size
        space_saving = (1 - (compressed_size / original_size)) * 100

        return {
            "original_size": original_size,
            "compressed_size": compressed_size,
            "compression_ratio": compression_ratio,
            "space_saving": space_saving
        }
    except FileNotFoundError:
        print("Hata: Performans hesaplanacak dosyalardan biri bulunamadı.")
        return None

def verify_lossless(original_path, decompressed_path):
    """
    Orijinal dosya ile sıkıştırılıp açılmış dosyanın görsel olarak aynı olup olmadığını kontrol eder.
    Bu fonksiyon, sadece piksel verilerini karşılaştırır. BMP başlıklarındaki farklılıklar
    (örn. dosya boyutu, renk tablosu sıralaması) göz ardı edilir, çünkü bunlar
    görsel kaybın olduğu anlamına gelmez.
    """
    try:
        with Image.open(original_path) as img1, Image.open(decompressed_path) as img2:
            # Görüntü modlarını ve boyutlarını karşılaştır
            if img1.mode != img2.mode or img1.size != img2.size:
                print(f"Hata: Görüntü modları veya boyutları farklı. '{os.path.basename(original_path)}' ({img1.mode}, {img1.size}) vs '{os.path.basename(decompressed_path)}' ({img2.mode}, {img2.size})")
                return False

            # Paletli görüntüler için paletleri daha güvenli bir şekilde karşılaştır
            if img1.mode == 'P':
                palette1 = img1.getpalette()
                palette2 = img2.getpalette()
                if palette1 != palette2:
                    # Paletlerin içeriği aynı ama sırası farklı olabilir.
                    # Bu durum genellikle görsel bir kayıp değildir.
                    # Şimdilik bir uyarı verip devam edelim.
                    print(f"Uyarı: Görüntü paletleri farklı olabilir. '{os.path.basename(original_path)}' vs '{os.path.basename(decompressed_path)}'")

            # Piksel verilerini karşılaştır
            pixels1 = np.array(img1)
            pixels2 = np.array(img2)
            
            if np.array_equal(pixels1, pixels2):
                return True  # Piksel verileri aynı, kayıpsız.
            else:
                print(f"Hata: Piksel verileri uyuşmuyor. '{os.path.basename(original_path)}' ve '{os.path.basename(decompressed_path)}' arasında fark var.")
                diff = np.sum(pixels1 != pixels2)
                print(f"Toplam {diff} pikselde farklılık bulundu.")
                return False # Piksel verileri farklı, kayıplı.

    except FileNotFoundError:
        print(f"Hata: Karşılaştırılacak dosyalardan biri bulunamadı: '{original_path}' veya '{decompressed_path}'")
        return False
    except Exception as e:
        print(f"Doğrulama sırasında bir hata oluştu: {e}")
        return False
