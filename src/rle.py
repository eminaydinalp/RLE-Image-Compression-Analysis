
"""
PackBits RLE (Run-Length Encoding) Algoritması
Bu algoritma, TIFF standardında kullanılan bir sıkıştırma yöntemidir.
Veriyi, "literal" (olduğu gibi yazılan) ve "run" (tekrarlanan) paketler
halinde kodlar.

Kontrol Baytı (n):
- 0 <= n <= 127: Literal Paket. Sonraki n+1 baytı olduğu gibi kopyala.
- -127 <= n <= -1: Tekrar Paketi. Sonraki baytı 1-n kez tekrar et.
- n = -128: No-op (boş işlem).
"""

def encode_packbits(data):
    """
    Verilen bir byte dizisini PackBits algoritması ile sıkıştırır.
    """
    if not data:
        return bytearray()

    encoded = bytearray()
    i = 0
    n = len(data)

    while i < n:
        # Literal verileri biriktirmek için bir tampon
        literals = []
        
        # Tekrarlanmayan veya kısa tekrarlı verileri bul ve biriktir
        while (i < n and (
               # Son iki bayta gelmediysek ve 3'lü tekrar yoksa
               (i + 2 >= n or not (data[i] == data[i+1] == data[i+2])) and
               # Tampon 128'e ulaşmadıysa
               len(literals) < 128)):
            literals.append(data[i])
            i += 1
        
        # Birikmiş literalleri yaz
        if literals:
            # Kontrol baytı: literal sayısı - 1
            encoded.append(len(literals) - 1)
            encoded.extend(literals)

        # Eğer döngüden tekrar nedeniyle çıktıysak, tekrar paketini işle
        if i < n:
            run_start = i
            # Tekrar eden baytın sonunu bul
            while i < n and data[i] == data[run_start] and (i - run_start) < 128:
                i += 1
            
            run_length = i - run_start
            # Kontrol baytı: -(tekrar sayısı - 1)
            # Negatif sayıyı geçerli bir byte değerine dönüştür (2'nin tümleyeni)
            control_byte = -(run_length - 1)
            encoded.append(control_byte & 255)
            encoded.append(data[run_start])

    return encoded


def decode_packbits(encoded_data):
    """
    PackBits ile sıkıştırılmış bir byte dizisini açar.
    """
    decoded = bytearray()
    i = 0
    n = len(encoded_data)

    while i < n:
        control_byte = encoded_data[i]
        i += 1

        # Gelen byte'ı signed değere çevir
        if control_byte > 127:
            control_byte -= 256

        if -127 <= control_byte <= -1:
            # Tekrar Paketi
            # Sonraki baytı (1 - control_byte) kez tekrar et
            repeat_count = 1 - control_byte
            value = encoded_data[i]
            i += 1
            decoded.extend([value] * repeat_count)
        elif 0 <= control_byte <= 127:
            # Literal Paket
            # Sonraki (control_byte + 1) baytı olduğu gibi kopyala
            length = control_byte + 1
            decoded.extend(encoded_data[i : i + length])
            i += length
        # control_byte == -128 (no-op) ise atlanır

    return decoded
