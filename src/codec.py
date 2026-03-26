
import os
import struct
import numpy as np
from PIL import Image

from . import rle
from . import traversal

# --- Yardımcı Fonksiyonlar ---

def get_bmp_header_and_pixels(file_path):
    """
    Bir BMP dosyasını okur, başlık (header) ve piksel matrisini ayırır.
    Pillow kütüphanesi, farklı BMP türlerini doğru şekilde işlemek için kullanılır.
    """
    with open(file_path, 'rb') as f:
        # BMP standardına göre piksel verisinin başlangıç ofseti 10. bayttadır.
        f.seek(10)
        pixel_data_offset = struct.unpack('<I', f.read(4))[0]
        
        # Başa dön ve başlığı oku
        f.seek(0)
        header = f.read(pixel_data_offset)

    # Pillow kullanarak pikselleri güvenli bir şekilde oku
    with Image.open(file_path) as img:
        # Görüntüyü numpy dizisine çevir
        pixels = np.array(img)
        height, width = pixels.shape[0], pixels.shape[1]
        mode = img.mode

    return header, pixels, width, height, mode

# --- Ana Sıkıştırma ve Açma Fonksiyonları ---

def compress_file(input_path, output_path, traversal_method='row'):
    """
    Bir BMP dosyasını sıkıştırır.
    
    1. BMP başlığını ve piksellerini ayırır.
    2. Belirtilen traversal metoduyla pikselleri 1D dizisine çevirir.
    3. PackBits RLE ile sıkıştırır.
    4. Özel bir formatta kaydeder:
       [Genişlik (4 byte)][Yükseklik (4 byte)][Traversal ID (1 byte)][BMP Başlığı][Sıkıştırılmış Veri]
    """
    try:
        # 1. BMP başlığını ve pikselleri al
        bmp_header, pixel_matrix, width, height, _ = get_bmp_header_and_pixels(input_path)
        
        # 2. Traversal metodunu seç ve uygula
        if traversal_method == 'row':
            traversal_func = traversal.traverse_row_by_row
            traversal_id = 0
        elif traversal_method == 'column':
            traversal_func = traversal.traverse_col_by_col
            traversal_id = 1
        elif traversal_method == 'zigzag':
            traversal_func = traversal.traverse_zigzag
            traversal_id = 2
        else:
            raise ValueError(f"Bilinmeyen traversal metodu: {traversal_method}")
            
        flat_pixels = traversal_func(pixel_matrix)
        
        # 3. RLE ile sıkıştır
        # .tobytes() ile numpy dizisini byte dizisine çevir
        compressed_data = rle.encode_packbits(flat_pixels.tobytes())
        
        # 4. Özel formatta dosyayı yaz
        with open(output_path, 'wb') as f:
            # Genişlik ve yüksekliği 4 byte'lık integer olarak yaz (<I: little-endian unsigned int)
            f.write(struct.pack('<II', width, height))
            # Traversal metodunun ID'sini 1 byte olarak yaz
            f.write(struct.pack('<B', traversal_id))
            # Orijinal BMP başlığını yaz
            f.write(bmp_header)
            # Sıkıştırılmış piksel verisini yaz
            f.write(compressed_data)
            
        print(f"'{os.path.basename(input_path)}' -> '{os.path.basename(output_path)}' olarak sıkıştırıldı ({traversal_method}).")

    except Exception as e:
        print(f"Sıkıştırma sırasında hata: {e}")


def decompress_file(input_path, output_path):
    """
    Sıkıştırılmış dosyayı açar ve orijinal BMP dosyasını yeniden oluşturur.
    """
    try:
        with open(input_path, 'rb') as f:
            # 1. Özel başlığı oku
            width, height = struct.unpack('<II', f.read(8))
            traversal_id = struct.unpack('<B', f.read(1))[0]
            
            # BMP başlığının başlangıcını bul
            # BMP başlığının boyutu, piksel ofsetinden gelir.
            # Bu bilgiyi okumak için geçici olarak başlığın bir kısmını okuyoruz.
            temp_header_start = f.tell()
            f.seek(temp_header_start + 10)
            pixel_data_offset = struct.unpack('<I', f.read(4))[0]
            
            # Başa dön ve gerçek başlığı ve sıkıştırılmış veriyi oku
            f.seek(temp_header_start)
            bmp_header = f.read(pixel_data_offset)
            compressed_data = f.read()

        # 2. RLE verisini aç
        decoded_bytes = rle.decode_packbits(compressed_data)
        
        # Byte dizisini orijinal veri tipine sahip numpy dizisine çevir
        # 1-bit ve 4-bit BMP'ler paletli (8-bit) olarak okunur, bu yüzden dtype='uint8' güvenlidir.
        flat_pixels = np.frombuffer(decoded_bytes, dtype=np.uint8)

        # 3. Inverse traversal uygula
        if traversal_id == 0:
            inverse_func = traversal.inverse_traverse_row_by_row
        elif traversal_id == 1:
            inverse_func = traversal.inverse_traverse_col_by_col
        else: # traversal_id == 2
            inverse_func = traversal.inverse_traverse_zigzag
            
        pixel_matrix = inverse_func(flat_pixels, height, width)
        
        # 4. Yeni BMP dosyasını oluştur
        # Pillow kullanarak pikselleri ve başlığı birleştirmek yerine,
        # doğrudan byte'ları birleştirmek daha güvenilirdir.
        
        # Pillow ile numpy dizisinden bir görüntü oluştur
        # Not: Paletli modlar ('P') için palet bilgisi de gerekir.
        # Ancak başlığı koruduğumuz için, sadece piksel verisini yazmak yeterli.
        # Bu kısım yerine doğrudan byte'ları birleştirelim.
        
        with open(output_path, 'wb') as f:
            f.write(bmp_header)
            f.write(pixel_matrix.tobytes())

        print(f"'{os.path.basename(input_path)}' -> '{os.path.basename(output_path)}' olarak açıldı.")

    except Exception as e:
        print(f"Açma sırasında hata: {e}")
