# RLE Görüntü Sıkıştırma Analizi

Bu proje, Çalışma Uzunluğu Kodlaması (Run-Length Encoding - RLE) yöntemini kullanarak farklı görüntü türleri üzerindeki sıkıştırma performansını analiz eder. Proje, bir girdi görüntüsünü alır, farklı formatlara dönüştürür, RLE ile sıkıştırır ve sonuçları değerlendirir.

## Proje Yapısı

- `input/`: Girdi görüntülerinin bulunduğu dizin.
- `generated_bmp/`: Girdi görüntüsünden oluşturulan farklı BMP formatlarındaki (siyah-beyaz, 4-bit grayscale, 8-bit renkli) görüntülerin bulunduğu dizin.
- `encoded/`: RLE ile ve farklı gezinme (traversal) yöntemleri (satır, sütun, zigzag) kullanılarak sıkıştırılmış dosyaların (`.myrle`) bulunduğu dizin.
- `decoded/`: Sıkıştırılmış dosyalardan geri elde edilen görüntülerin bulunduğu dizin.
- `results/`: Sıkıştırma analizi sonuçlarının (örneğin, sıkıştırma oranı, süre) bulunduğu dizin.
- `src/`: Projenin Python kaynak kodlarının bulunduğu dizin.
  - `main.py`: Tüm süreci başlatan ana betik.
  - `convert_bmp.py`: Görüntü formatı dönüşümlerini yapar.
  - `rle.py`: RLE sıkıştırma ve açma mantığını içerir.
  - `traversal.py`: Farklı piksel gezinme stratejilerini (satır-satır, sütun-sütun, zigzag) içerir.
  - `codec.py`: Kodlama ve kod çözme işlemlerini yönetir.
  - `evaluate.py`: Sıkıştırma performansını değerlendirir.
- `Odev.md`: Proje ödevi ile ilgili detaylı bilgileri içeren dosyadır.


