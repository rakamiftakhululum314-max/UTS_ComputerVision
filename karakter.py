import numpy as np
import cv2
import os

# Buat folder output jika belum ada
if not os.path.exists('output'):
    os.makedirs('output')

def create_character():
    """Membuat karakter robot sederhana"""
    # Buat kanvas putih
    canvas = np.full((400, 400, 3), 255, dtype=np.uint8)
    
    # Gambar kepala (lingkaran)
    cv2.circle(canvas, (200, 120), 60, (0, 100, 200), -1)  # Kepala oranye
    cv2.circle(canvas, (200, 120), 60, (0, 0, 0), 2)       # Outline kepala
    
    # Gambar mata (dua lingkaran kecil)
    cv2.circle(canvas, (180, 110), 10, (255, 255, 255), -1)  # Mata kiri
    cv2.circle(canvas, (220, 110), 10, (255, 255, 255), -1)  # Mata kanan
    cv2.circle(canvas, (180, 110), 5, (0, 0, 0), -1)        # Pupil kiri
    cv2.circle(canvas, (220, 110), 5, (0, 0, 0), -1)        # Pupil kanan
    
    # Gambar senyum (garis)
    cv2.ellipse(canvas, (200, 140), (30, 15), 0, 0, 180, (0, 0, 0), 2)
    
    # Gambar badan (persegi panjang)
    cv2.rectangle(canvas, (150, 180), (250, 300), (100, 150, 200), -1)  # Badan biru
    cv2.rectangle(canvas, (150, 180), (250, 300), (0, 0, 0), 2)         # Outline badan
    
    # Gambar tangan (garis)
    cv2.line(canvas, (150, 200), (100, 250), (0, 0, 0), 5)   # Tangan kiri
    cv2.line(canvas, (250, 200), (300, 250), (0, 0, 0), 5)   # Tangan kanan
    
    # Gambar kaki (persegi panjang)
    cv2.rectangle(canvas, (170, 300), (190, 350), (0, 0, 0), -1)  # Kaki kiri
    cv2.rectangle(canvas, (210, 300), (230, 350), (0, 0, 0), -1)  # Kaki kanan
    
    # Tambahkan teks
    cv2.putText(canvas, 'ROBOT', (160, 370), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    return canvas

def apply_transformations(character):
    """Menerapkan berbagai transformasi pada karakter"""
    
    # 1. Translation (Geser posisi)
    height, width = character.shape[:2]
    translation_matrix = np.float32([[1, 0, 50], [0, 1, 30]])  # Geser 50px kanan, 30px bawah
    translated = cv2.warpAffine(character, translation_matrix, (width, height))
    cv2.imwrite('output/translated.png', translated)
    
    # 2. Rotasi (Putar 45 derajat)
    center = (width // 2, height // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, 45, 1.0)  # Rotasi 45 derajat
    rotated = cv2.warpAffine(character, rotation_matrix, (width, height))
    cv2.imwrite('output/rotated.png', rotated)
    
    # 3. Resize (Ubah ukuran menjadi setengah)
    resized = cv2.resize(character, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
    cv2.imwrite('output/resized.png', resized)
    
    # 4. Crop (Potong sebagian gambar - area wajah)
    cropped = character[50:200, 150:250]  # [y1:y2, x1:x2]
    cv2.imwrite('output/cropped.png', cropped)
    
    return translated, rotated, resized, cropped

def apply_operations(character):
    """Menerapkan operasi aritmatika dan bitwise"""
    
    # Buat background gradient untuk operasi
    background = np.zeros((400, 400, 3), dtype=np.uint8)
    for i in range(400):
        background[i, :] = [i//2, i//3, i//4]  # Gradient biru-hijau
    
    # 1. Operasi Aritmatika - cv2.add() (Menambahkan karakter dengan background)
    added = cv2.add(character, background)
    cv2.imwrite('output/added.png', added)
    
    # 2. Operasi Aritmatika - cv2.subtract() 
    subtracted = cv2.subtract(character, background)
    cv2.imwrite('output/subtracted.png', subtracted)
    
    # 3. Operasi Bitwise - cv2.bitwise_and()
    # Buat mask dari karakter (konversi ke grayscale dulu)
    gray = cv2.cvtColor(character, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    
    # Aplikasikan bitwise operations
    bg_region = cv2.bitwise_and(background, background, mask=mask_inv)
    fg_region = cv2.bitwise_and(character, character, mask=mask)
    bitwise_combined = cv2.add(bg_region, fg_region)
    cv2.imwrite('output/bitwise.png', bitwise_combined)
    
    # 4. Operasi Bitwise - cv2.bitwise_or()
    bitwise_or = cv2.bitwise_or(character, background)
    cv2.imwrite('output/bitwise_or.png', bitwise_or)
    
    return added, subtracted, bitwise_combined, bitwise_or

def create_final_composition():
    """Membuat komposisi final dari semua hasil"""
    
    # Buat kanvas besar untuk menampilkan semua hasil
    final_canvas = np.full((900, 1200, 3), 255, dtype=np.uint8)
    
    # Buat karakter asli
    character = create_character()
    
    # Aplikasikan transformasi
    translated, rotated, resized, cropped = apply_transformations(character)
    
    # Aplikasikan operasi
    added, subtracted, bitwise_combined, bitwise_or = apply_operations(character)
    
    # Tampilkan semua hasil di canvas final
    final_canvas[50:450, 50:450] = character                    # Original
    final_canvas[50:450, 500:900] = rotated                     # Rotated
    final_canvas[500:700, 50:250] = resized                     # Resized
    final_canvas[500:650, 300:400] = cropped                    # Cropped
    final_canvas[500:900, 500:900] = bitwise_combined           # Bitwise
    
    # Tambahkan label
    fonts = [cv2.FONT_HERSHEY_SIMPLEX, cv2.FONT_HERSHEY_PLAIN, 
             cv2.FONT_HERSHEY_DUPLEX, cv2.FONT_HERSHEY_COMPLEX]
    
    cv2.putText(final_canvas, 'Original', (180, 40), fonts[0], 1, (0,0,0), 2)
    cv2.putText(final_canvas, 'Rotated 45', (630, 40), fonts[0], 1, (0,0,0), 2)
    cv2.putText(final_canvas, 'Resized 50%', (80, 480), fonts[0], 0.7, (0,0,0), 2)
    cv2.putText(final_canvas, 'Cropped', (320, 480), fonts[0], 0.7, (0,0,0), 2)
    cv2.putText(final_canvas, 'Bitwise Combined', (630, 480), fonts[0], 0.7, (0,0,0), 2)
    
    cv2.imwrite('output/final.png', final_canvas)
    
    return final_canvas

def display_results():
    """Menampilkan semua hasil"""
    images = {}
    
    # Load semua gambar yang telah disimpan
    image_files = ['karakter.png', 'translated.png', 'rotated.png', 
                   'resized.png', 'cropped.png', 'bitwise.png', 'final.png']
    
    for img_file in image_files:
        img_path = os.path.join('output', img_file)
        if os.path.exists(img_path):
            images[img_file] = cv2.imread(img_path)
    
    # Tampilkan gambar satu per satu
    for name, img in images.items():
        cv2.imshow(name, img)
        cv2.waitKey(500)  # Tampilkan setiap 0.5 detik
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    print("Membuat karakter...")
    
    # Buat karakter
    character = create_character()
    cv2.imwrite('output/karakter.png', character)
    print("✓ Karakter berhasil dibuat dan disimpan sebagai 'output/karakter.png'")
    
    # Aplikasikan transformasi
    print("Menerapkan transformasi...")
    apply_transformations(character)
    print("✓ Transformasi berhasil diterapkan")
    
    # Aplikasikan operasi
    print("Menerapkan operasi aritmatika dan bitwise...")
    apply_operations(character)
    print("✓ Operasi berhasil diterapkan")
    
    # Buat komposisi final
    print("Membuat komposisi final...")
    create_final_composition()
    print("✓ Komposisi final berhasil dibuat")
    
    # Tampilkan hasil
    print("Menampilkan hasil...")
    display_results()
    print("✓ Program selesai!")
    
    print("\nFile yang dihasilkan:")
    for file in os.listdir('output'):
        print(f"  - output/{file}")

if __name__ == "__main__":
    main()