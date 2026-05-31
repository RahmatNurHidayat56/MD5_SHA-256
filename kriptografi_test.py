import hashlib
import os

def hitung_hash(nama_file):
    """Menghitung hash MD5 dan SHA-256 dari sebuah file"""
    md5_hash = hashlib.md5()
    sha256_hash = hashlib.sha256()
    
    try:
        with open(nama_file, "rb") as f:
            # Membaca file dalam bentuk chunk (blok) agar efisien untuk file besar
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
                sha256_hash.update(chunk)
        return md5_hash.hexdigest(), sha256_hash.hexdigest()
    except FileNotFoundError:
        print(f"Error: File '{nama_file}' tidak ditemukan.")
        return None, None

def cek_integritas(file_asli, file_modifikasi):
    """Membandingkan hash dari dua file untuk mengecek perubahan"""
    print("=" * 60)
    print("      APLIKASI PENGECEKAN INTEGRITAS FILE (MD5 & SHA-256)      ")
    print("=" * 60)
    
    # 1. Hitung hash file asli
    print(f"\n[+] Memproses File Asli: {file_asli}")
    md5_asli, sha256_asli = hitung_hash(file_asli)
    if not md5_asli: return
    print(f"    - MD5    : {md5_asli}")
    print(f"    - SHA-256: {sha256_asli}")
    
    # 2. Hitung hash file yang dimodifikasi
    print(f"\n[+] Memproses File Dimodifikasi: {file_modifikasi}")
    md5_mod, sha256_mod = hitung_hash(file_modifikasi)
    if not md5_mod: return
    print(f"    - MD5    : {md5_mod}")
    print(f"    - SHA-256: {sha256_mod}")
    
    # 3. Membandingkan perubahan file
    print("\n" + "=" * 60)
    print("HASIL ANALISIS PERBANDINGAN FILE:")
    print("=" * 60)
    
    if md5_asli == md5_mod and sha256_asli == sha256_mod:
        print(" STATUS: INTEGRITAS TERJAGA (VALID)")
        print(" Keterangan: Nilai hash identik. File TIDAK mengalami perubahan.")
    else:
        print(" STATUS: INTEGRITAS RUSAK / FILE TELAH DIUBAH (PERINGATAN!)")
        print(" Keterangan: Nilai hash BERBEDA. File telah dimodifikasi!")
        
        # Detail perbedaan
        if md5_asli != md5_mod:
            print("   -> Perubahan terdeteksi melalui MD5")
        if sha256_asli != sha256_mod:
            print("   -> Perubahan terdeteksi melalui SHA-256")
    print("=" * 60)

# --- Skenario Simulasi ---
if __name__ == "__main__":
    file_1 = "dokumen_asli.txt"
    file_2 = "dokumen_modifikasi.txt"
    
    # Membuat file simulasi otomatis untuk keperluan testing
    with open(file_1, "w") as f:
        f.write("Ini adalah pesan rahasia yang sangat penting.")
        
    with open(file_2, "w") as f:
        f.write("Ini adalah pesan rahasia yang sangat penting!") # Berbeda 1 karakter (tanda seru)
        
    # Jalankan pengecekan
    cek_integritas(file_1, file_2)
    
    # Membersihkan file temporary setelah pengujian selesai
    if os.path.exists(file_1): os.remove(file_1)
    if os.path.exists(file_2): os.remove(file_2)