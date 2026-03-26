
import os
import pandas as pd
from tabulate import tabulate
import time

# Projenin diğer modüllerini import et
from . import codec
from . import evaluate
from . import convert_bmp

# --- Proje Dizinlerini Tanımla ---
# Bu dosyanın bulunduğu dizin 'src'. Proje ana dizini bir üst seviyede.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(BASE_DIR, 'generated_bmp')
ENCODED_DIR = os.path.join(BASE_DIR, 'encoded')
DECODED_DIR = os.path.join(BASE_DIR, 'decoded')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')

def main():
    """
    Ana otomasyon betiği.
    1. Gerekli BMP dosyalarını oluşturur.
    2. Tanımlanan tüm deneyleri (BMP tipi x Traversal metodu) yürütür.
    3. Her deney için sıkıştırma, açma ve değerlendirme adımlarını çalıştırır.
    4. Sonuçları bir tablo halinde konsola basar ve dosyaya kaydeder.
    """
    start_time = time.time()

    # --- Adım 1: Gerekli Klasörlerin ve BMP'lerin Oluşturulması ---
    print("--- Adım 1: Gerekli dosyalar ve klasörler hazırlanıyor...")
    os.makedirs(ENCODED_DIR, exist_ok=True)
    os.makedirs(DECODED_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    # convert_bmp.py'deki main fonksiyonunu çağırarak BMP'lerin hazır olduğundan emin ol
    convert_bmp.main()
    print("-" * 50)

    # --- Adım 2: Deneylerin Tanımlanması ---
    # Deneyler: (BMP Dosya Adı, BMP Tipi Açıklaması)
    experiments = [
        ('black_and_white.bmp', 'Black & White'),
        ('4bit_grayscale.bmp', '4-bit Grayscale'),
        ('color_table.bmp', 'Color Table (8-bit)'),
    ]
    
    # Dolaşma metodları
    traversal_methods = ['row', 'column', 'zigzag']
    
    # Sonuçları saklamak için bir liste
    results_list = []

    # --- Adım 3: Tüm Deneyleri Döngü İçinde Çalıştır ---
    print("--- Adım 2: Sıkıştırma ve Değerlendirme Deneyleri Başlatılıyor...")
    for bmp_filename, bmp_type_desc in experiments:
        for method in traversal_methods:
            print(f"\n-> Deney: BMP Tipi='{bmp_type_desc}', Okuma='{method.capitalize()}'")
            
            # Dosya yollarını oluştur
            original_file = os.path.join(INPUT_DIR, bmp_filename)
            compressed_file = os.path.join(ENCODED_DIR, f"{os.path.splitext(bmp_filename)[0]}_{method}.myrle")
            decompressed_file = os.path.join(DECODED_DIR, f"{os.path.splitext(bmp_filename)[0]}_{method}_decoded.bmp")

            # --- Sıkıştırma, Açma ve Değerlendirme ---
            # Sıkıştır
            codec.compress_file(original_file, compressed_file, traversal_method=method)
            
            # Aç
            codec.decompress_file(compressed_file, decompressed_file)
            
            # Performansı Hesapla
            performance = evaluate.calculate_performance(original_file, compressed_file)
            
            # Kayıpsızlığı Doğrula
            is_lossless = evaluate.verify_lossless(original_file, decompressed_file)
            
            # Sonuçları listeye ekle
            if performance:
                results_list.append({
                    "BMP Tipi": bmp_type_desc,
                    "Okuma Yöntemi": method.capitalize(),
                    "Orijinal Boyut (byte)": f"{performance['original_size']:,}",
                    "Sıkıştırılmış Boyut (byte)": f"{performance['compressed_size']:,}",
                    "Sıkıştırma Oranı": f"{performance['compression_ratio']:.2f}x",
                    "Yer Kazancı (%)": f"{performance['space_saving']:.2f}%",
                    "Kayıpsız mı?": "Evet" if is_lossless else "HAYIR!"
                })

    print("-" * 50)
    print("--- Adım 3: Sonuçlar Hazırlanıyor...")

    # --- Adım 4: Sonuçları Tablo Olarak Sun ---
    if not results_list:
        print("Hiçbir sonuç üretilemedi. Lütfen hataları kontrol edin.")
        return

    # Pandas DataFrame oluştur
    df = pd.DataFrame(results_list)
    
    # Tabloyu konsola güzel bir formatta yazdır
    print("\n" + "="*20 + " SIKIŞTIRMA SONUÇLARI " + "="*20)
    print(tabulate(df, headers='keys', tablefmt='grid', stralign="center"))
    
    # Tabloyu bir metin dosyasına ve CSV dosyasına kaydet
    table_txt_path = os.path.join(RESULTS_DIR, 'sonuclar_tablosu.txt')
    table_csv_path = os.path.join(RESULTS_DIR, 'sonuclar_tablosu.csv')
    
    with open(table_txt_path, 'w', encoding='utf-8') as f:
        f.write(tabulate(df, headers='keys', tablefmt='pipe'))
        
    df.to_csv(table_csv_path, index=False)
    
    end_time = time.time()
    print(f"\nSonuçlar '{RESULTS_DIR}' klasörüne kaydedildi.")
    print(f"Tüm işlemler {end_time - start_time:.2f} saniyede tamamlandı.")


if __name__ == '__main__':
    main()
