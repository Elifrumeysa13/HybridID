import os
import exifread

def detect_ai_signature(tags: dict) -> tuple[bool, list[str]]:
    """
    EXIF etiketlerini analiz ederek bilinen AI (Yapay Zeka) araçlarının yazılım izlerini tespit eder.
    
    Args:
        tags (dict): Görselden çıkarılan EXIF etiketlerini içeren sözlük.
        
    Returns:
        tuple[bool, list[str]]: Şüpheli bir iz bulunup bulunmadığını (True/False) ve 
                                bulunan izlerin detaylarını içeren bir liste döner.
    """
    ai_keywords = [
        "midjourney", "dall-e", "stable diffusion", "adobe firefly", 
        "ai generated", "openai", "comfyui", "leonardo"
    ]
    
    critical_tags = [
        "Image Software", "Image CreatorTool", "EXIF UserComment", 
        "Image ImageDescription", "Image Make", "Image Model",
        "Software", "CreatorTool", "UserComment", "ImageDescription", "Make", "Model"
    ]
    
    found_signatures = []
    
    for tag_name in critical_tags:
        if tag_name in tags:
            tag_value = str(tags[tag_name]).lower()
            for keyword in ai_keywords:
                if keyword in tag_value:
                    found_signatures.append(
                        f"Şüpheli iz '{keyword}', şu etikette bulundu: '{tag_name}' -> {tags[tag_name]}"
                    )
                    
    return len(found_signatures) > 0, found_signatures

def analyze_metadata(file_path: str) -> dict:
    """
    Belirtilen görsel dosyasının EXIF/Metadata'sını çıkarır, AI yazılım izlerini arar 
    ve sonucu ekrana okunabilir (human-readable) formatta yazdırır.
    
    Args:
        file_path (str): İncelenecek görselin dosya yolu.
        
    Returns:
        dict: Çıkarılan tüm EXIF etiketlerini içeren sözlük. Hata durumunda veya veri bulunmazsa boş sözlük döner.
    """
    if not os.path.exists(file_path):
        print(f"Hata: İncelenecek dosya bulunamadı -> {file_path}")
        return {}
        
    tags = {}
    try:
        # Görsel, gereksinimlerde belirtildiği üzere ikili (binary) modda (rb) okunuyor
        with open(file_path, 'rb') as image_file:
            tags = exifread.process_file(image_file)
            
        if not tags:
            print("Uyarı: Metadata bulunamadı (EXIF verisi temizlenmiş olabilir veya desteklenmeyen format).")
            return {}
            
        print(f"\n--- Metadata Analiz Raporu: {file_path} ---")
        print(f"Toplam {len(tags)} EXIF etiketi başarıyla çıkarıldı.")
        
        # AI yazılım izi kontrolü yapılıyor
        is_ai, signatures = detect_ai_signature(tags)
        
        if is_ai:
            print("\n[!] Şüpheli Yazılım İzi Bulundu [!]")
            for sig in signatures:
                print(f" - {sig}")
            print("-" * 45)
        else:
            print("\n[+] Temiz: Bilinen bir AI aracı izine rastlanmadı.")
            
        # Temiz ve okunabilir bir çıktı (Clean Output) için bazı önemli etiketleri özetleyelim
        print("\nÖnemli Metadata Detayları:")
        important_tags = [
            "Image Make", "Image Model", "Image Software", 
            "Image DateTime", "EXIF ExifImageWidth", "EXIF ExifImageLength"
        ]
        
        for tag in important_tags:
            if tag in tags:
                print(f"{tag:<25}: {tags[tag]}")
                
        print("-------------------------------------------\n")
        return tags
        
    except Exception as e:
        print(f"Hata: Dosya işlenirken beklenmeyen bir sorun oluştu: {e}")
        return {}

if __name__ == "__main__":
    # Başına 'r' koyarak yolu temizliyoruz
    test_image_path = r"C:\Users\demir\Desktop\HybridID\test_images\Test.jpg"
    print("--- Analiz Başlatılıyor ---")
    analyze_metadata(test_image_path)