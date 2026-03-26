
import numpy as np

# --- Traversal Fonksiyonları (Okuma) ---

def traverse_row_by_row(pixel_matrix):
    """
    Piksel matrisini satır satır düz bir diziye çevirir.
    """
    return pixel_matrix.flatten()

def traverse_col_by_col(pixel_matrix):
    """
    Piksel matrisini sütun sütun düz bir diziye çevirir.
    'F' (Fortran-like) order ile sütun öncelikli düzleştirme yapılır.
    """
    return pixel_matrix.flatten('F')

def traverse_zigzag(pixel_matrix, block_size=64):
    """
    Piksel matrisini block_size'lık bloklara bölerek zigzag desende okur.
    """
    height, width = pixel_matrix.shape
    stream = []
    
    for y_start in range(0, height, block_size):
        for x_start in range(0, width, block_size):
            # Blok sınırlarını belirle
            y_end = min(y_start + block_size, height)
            x_end = min(x_start + block_size, width)
            block = pixel_matrix[y_start:y_end, x_start:x_end]
            
            # Blok içinde zigzag dolaş
            stream.extend(_zigzag_scan(block))
            
    return np.array(stream)

def _zigzag_scan(block):
    """
    Verilen bir blok içinde zigzag deseninde dolaşarak elemanları bir listeye ekler.
    """
    rows, cols = block.shape
    result = []
    row, col = 0, 0
    going_up = True

    while len(result) < rows * cols:
        result.append(block[row, col])
        
        if going_up:
            if col == cols - 1:
                row += 1
                going_up = False
            elif row == 0:
                col += 1
                going_up = False
            else:
                row -= 1
                col += 1
        else: # going_down
            if row == rows - 1:
                col += 1
                going_up = True
            elif col == 0:
                row += 1
                going_up = True
            else:
                row += 1
                col -= 1
                
    return result

# --- Inverse Traversal Fonksiyonları (Yeniden Oluşturma) ---

def inverse_traverse_row_by_row(flat_array, height, width):
    """
    Satır satır okunmuş düz diziyi orijinal matris boyutlarına geri getirir.
    """
    return flat_array.reshape((height, width))

def inverse_traverse_col_by_col(flat_array, height, width):
    """
    Sütun sütun okunmuş düz diziyi orijinal matris boyutlarına geri getirir.
    """
    return flat_array.reshape((height, width), order='F')

def inverse_traverse_zigzag(flat_array, height, width, block_size=64):
    """
    Zigzag okunmuş düz diziyi orijinal matris boyutlarına geri getirir.
    """
    pixel_matrix = np.zeros((height, width), dtype=flat_array.dtype)
    stream_idx = 0
    
    for y_start in range(0, height, block_size):
        for x_start in range(0, width, block_size):
            y_end = min(y_start + block_size, height)
            x_end = min(x_start + block_size, width)
            
            block_height = y_end - y_start
            block_width = x_end - x_start
            
            block_size_flat = block_height * block_width
            block_stream = flat_array[stream_idx : stream_idx + block_size_flat]
            
            # Düz diziden bloğu yeniden oluştur
            block = _inverse_zigzag_scan(block_stream, block_height, block_width)
            pixel_matrix[y_start:y_end, x_start:x_end] = block
            
            stream_idx += block_size_flat
            
    return pixel_matrix

def _inverse_zigzag_scan(flat_block, rows, cols):
    """
    Düz bir blok dizisini zigzag desenini tersine çevirerek 2D bir bloğa dönüştürür.
    """
    block = np.zeros((rows, cols), dtype=flat_block.dtype)
    row, col = 0, 0
    going_up = True
    
    for i in range(len(flat_block)):
        block[row, col] = flat_block[i]
        
        if going_up:
            if col == cols - 1:
                row += 1
                going_up = False
            elif row == 0:
                col += 1
                going_up = False
            else:
                row -= 1
                col += 1
        else: # going_down
            if row == rows - 1:
                col += 1
                going_up = True
            elif col == 0:
                row += 1
                going_up = True
            else:
                row += 1
                col -= 1
                
    return block
