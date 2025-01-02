from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from selenium.common.exceptions import TimeoutException

def setup_driver():
    """Selenium WebDriver'ı yapılandır"""
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_profile_data(profile_name):
    """Belirtilen profil için verileri çeker"""
    driver = None
    
    def extract_value(text):
        """Metinden sayısal değeri çıkarır"""
        try:
            # Eşittir işaretinden sonraki kısmı al
            value_str = text.split('=')[1].strip().split()[0]
            print(f"İşlenecek değer: {value_str}")  # Debug
            
            # Bilimsel gösterim kontrolü
            if 'E+' in value_str or 'e+' in value_str:
                # Bilimsel gösterimi parçala
                parts = value_str.upper().split('E+')
                if len(parts) == 2:
                    base = float(parts[0].replace(',', '.'))
                    exponent = int(parts[1])
                    result = base * (10 ** exponent)
                    print(f"Bilimsel gösterim sonucu: {result}")  # Debug
                    return result
            else:
                # Normal sayı
                result = float(value_str.replace(',', '.'))
                print(f"Normal sayı sonucu: {result}")  # Debug
                return result
            
        except Exception as e:
            print(f"Değer çıkarma hatası: {str(e)}")
            return None
    
    # RHS, SHS, CHS profilleri için et kalınlığını profil adından çıkar
    def extract_thickness(profile_name):
        try:
            if profile_name.startswith(('RHS', 'SHS', 'CHS')):
                parts = profile_name.split('x')
                thickness = float(parts[-1])  # En son değer et kalınlığıdır
                return thickness
            return None
        except Exception as e:
            print(f"Et kalınlığı çıkarılamadı: {profile_name}, Hata: {str(e)}")
            return None
    
    try:
        driver = setup_driver()
        base_url = "https://www.staticstools.eu/en"
        
        # URL için profil adını düzenle
        if profile_name.startswith('HE') and profile_name.endswith('AA'):  # Önce HEAA kontrolü
            number_part = ''.join(filter(str.isdigit, profile_name))
            url_profile_name = f"HE{number_part}AA"
            url_path = "profile-heaa"
        elif profile_name.startswith('HE') and profile_name.endswith('A'):  # Sonra HEA kontrolü
            number_part = ''.join(filter(str.isdigit, profile_name))
            url_profile_name = f"HE{number_part}A"
            url_path = "profile-hea"
        elif profile_name.startswith('HE') and profile_name.endswith('B'):  # Sonra HEB kontrolü
            number_part = ''.join(filter(str.isdigit, profile_name))
            url_profile_name = f"HE{number_part}B"
            url_path = "profile-heb"
        elif profile_name.startswith('HE') and profile_name.endswith('M'):  # Son olarak HEM kontrolü
            number_part = ''.join(filter(str.isdigit, profile_name))
            url_profile_name = f"HE{number_part}M"
            url_path = "profile-hem"
        elif profile_name.startswith('IPN'):
            number_part = ''.join(filter(str.isdigit, profile_name))
            url_profile_name = f"IPN+{number_part}"
            url_path = "profile-ipn"
        elif profile_name.startswith('IPEAA'):
            number_part = ''.join(filter(str.isdigit, profile_name))
            url_profile_name = f"IPE+AA+{number_part}"
            url_path = "profile-ipeaa"
        elif profile_name.startswith('IPEA'):
            number_part = ''.join(filter(str.isdigit, profile_name))
            url_profile_name = f"IPEA{number_part}"
            url_path = "profile-ipea"
        elif profile_name.startswith('IPEO'):
            number_part = ''.join(filter(str.isdigit, profile_name))
            url_profile_name = f"IPEO{number_part}"
            url_path = "profile-ipeo"
        elif profile_name.startswith('IPE'):
            number_part = ''.join(filter(str.isdigit, profile_name))
            url_profile_name = f"IPE{number_part}"
            url_path = "profile-ipe"
        elif profile_name.startswith('UPN'):
            number_part = ''.join(filter(str.isdigit, profile_name))
            url_profile_name = f"UPN+{number_part}"
            url_path = "profile-upn"
        elif profile_name.startswith('UPE'):
            number_part = ''.join(filter(str.isdigit, profile_name))
            url_profile_name = f"UPE+{number_part}"
            url_path = "profile-upe"
        elif profile_name.startswith('UAP'):
            number_part = ''.join(filter(str.isdigit, profile_name))
            url_profile_name = f"UAP{number_part}"
            url_path = "profile-uap"
        elif profile_name.startswith('UE'):
            number_part = ''.join(filter(str.isdigit, profile_name))
            url_profile_name = f"UE{number_part}"
            url_path = "profile-ue"
        elif profile_name.startswith('HEAA'):
            number_part = ''.join(filter(str.isdigit, profile_name))
            url_profile_name = f"HE{number_part}AA"
            url_path = "profile-heaa"
        elif profile_name.startswith('HEA'):
            number_part = ''.join(filter(str.isdigit, profile_name))
            url_profile_name = f"HE{number_part}A"
            url_path = "profile-hea"
        elif profile_name.startswith('HEB'):
            number_part = ''.join(filter(str.isdigit, profile_name))
            url_profile_name = f"HE{number_part}B"
            url_path = "profile-heb"
        elif profile_name.startswith('HEM'):
            number_part = ''.join(filter(str.isdigit, profile_name))
            url_profile_name = f"HE{number_part}M"
            url_path = "profile-hem"
        elif profile_name.startswith('HD'):
            size_part = profile_name[2:]  # HD'yi kaldır
            url_profile_name = f"HD{size_part}"
            url_path = "profile-hd"
        elif profile_name.startswith('HL'):
            size_part = profile_name[2:]  # HL'yi kaldır
            url_profile_name = f"HL+{size_part}"
            url_path = "profile-hl"
        elif profile_name.startswith('LU'):
            size_part = profile_name[2:]  # LU'yu kaldır
            url_profile_name = f"L+{size_part}"
            url_path = "profile-lu"
        elif profile_name.startswith('L'):
            size_part = profile_name[1:]  # L'yi kaldır
            url_profile_name = f"L+{size_part}"
            url_path = "profile-le"
        elif profile_name.startswith('T'):
            size_part = profile_name[1:]  # T'yi kaldır
            url_profile_name = f"T{size_part}"
            url_path = "profile-t"
        elif profile_name.startswith('SHS'):
            size_part = profile_name[3:]  # SHS'yi kaldır
            url_profile_name = f"SHS+{size_part}"
            url_path = "profile-shs"
        elif profile_name.startswith('RHS'):
            size_part = profile_name[3:]  # RHS'yi kaldır
            url_profile_name = f"RHS+{size_part}"
            url_path = "profile-rhs"
        elif profile_name.startswith('CHS'):
            size_part = profile_name[3:]  # CHS'yi kaldır
            url_profile_name = f"CHS+{size_part}"
            url_path = "profile-chs"
        else:
            print(f"Bilinmeyen profil tipi: {profile_name}")
            return None

        url = f"{base_url}/{url_path}/{url_profile_name}/mm/show"
        print(f"URL: {url}")
        print(f"Veri alınıyor: {profile_name}")
        
        driver.get(url)
        time.sleep(2)  # Sayfanın yüklenmesi için biraz bekle
        
        # Önce sayfanın yüklendiğinden emin olalım
        wait = WebDriverWait(driver, 10)
        
        # Farklı tablo sınıf isimleri için kontrol
        try:
            tables = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "table")))
        except TimeoutException:
            # Eğer "table" sınıfı bulunamazsa diğer olası sınıfları dene
            try:
                tables = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "profile-table")))
            except TimeoutException:
                # Son çare olarak tüm tabloları bul
                tables = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "table")))
        
        print(f"Bulunan tablo sayısı: {len(tables)}")
        
        # Tabloları debug için yazdır
        for i, table in enumerate(tables):
            print(f"\nTablo {i+1}:")
            print(table.get_attribute('outerHTML')[:200] + "...")  # İlk 200 karakteri göster
        
        all_cells = []
        for table in tables:
            cells = table.find_elements(By.TAG_NAME, "td")
            all_cells.extend(cells)
            
        print(f"Toplam bulunan hücre sayısı: {len(all_cells)}")
        
        # Profil tipine göre dictionary yapısını belirle
        if profile_name.startswith('T'):
            data = {
                'Profil': profile_name,
                # Geometry
                'h = b (mm)': None,
                's = t (mm)': None,
                'r (mm)': None,
                'r1 (mm)': None,
                'r2 (mm)': None,
                'zs (mm)': None,
                "z's (mm)": None,
                'A (mm²)': None,
                'G (kg/m)': None,
                'AL (m²/m)': None,
                
                # Section properties
                'Iy (mm⁴)': None,
                'Wy1 (mm³)': None,
                'Wy2 (mm³)': None,
                'iy (mm)': None,
                'Iz (mm⁴)': None,
                'Wz (mm³)': None,
                'iz (mm)': None
            }
        elif profile_name.startswith('L'):
            data = {
                'Profil': profile_name,
                # Geometry
                'b (mm)': None,
                't (mm)': None,
                'r1 (mm)': None,
                'r2 (mm)': None,
                'ys (mm)': None,
                "y's (mm)": None,
                'v (mm)': None,
                'u1 (mm)': None,
                'u2 (mm)': None,
                'A (mm²)': None,
                'AL (m²/m)': None,
                'G (kg/m)': None,
                
                # Section properties - Axis y
                'Iy (mm⁴)': None,
                'Wy1 (mm³)': None,
                'Wy2 (mm³)': None,
                'iy (mm)': None,
                
                # Section properties - Axis z
                'Iz (mm⁴)': None,
                'Wz2 (mm³)': None,
                'Wz3 (mm³)': None,
                'iz (mm)': None,
                
                # Section properties - Main axes
                'Iu (mm⁴)': None,
                'Iv (mm⁴)': None,
                'Wu1 (mm³)': None,
                'Wv2 (mm³)': None,
                'Wv3 (mm³)': None,
                'iu (mm)': None,
                'iv (mm)': None,
                'um (mm)': None,
                
                # Warping and buckling
                'It (mm⁴)': None,
                'ipc (mm)': None,
                'ipa (mm)': None,
                'Iyz (mm⁴)': None
            }
        elif profile_name.startswith('CHS'):
            parts = profile_name.split('x')
            thickness = float(parts[-1]) if len(parts) == 2 else None
            
            data = {
                'Profil': profile_name,
                # Geometry
                'D (mm)': None,
                'T (mm)': thickness,
                'A (mm²)': None,
                'AL (m²/m)': None,
                'G (kg/m)': None,
                
                # Section properties
                'Iy (mm⁴)': None,
                'Iz (mm⁴)': None,
                'Wy,el (mm³)': None,
                'Wz,el (mm³)': None,
                'Wy,pl (mm³)': None,
                'Wz,pl (mm³)': None,
                'iy (mm)': None,
                'iz (mm)': None,
                
                # Warping and buckling
                'It (mm⁴)': None,
                'Ct (mm³)': None
            }
            
            # Kalınlık değerini hemen ata
            if thickness is not None:
                data['T (mm)'] = thickness
        elif profile_name.startswith('RHS'):
            # RHS50x30x2.6 formatından kalınlığı al
            parts = profile_name.split('x')
            thickness = float(parts[-1]) if len(parts) == 3 else None
            
            data = {
                'Profil': profile_name,
                'h (mm)': None,
                'b (mm)': None,
                't (mm)': thickness,  # Kalınlık değerini profil adından al
                'r (mm)': None,
                'A (mm²)': None,
                'AL (m²/m)': None,
                'G (kg/m)': None,
                
                # Section properties - Axis y
                'Iy (mm⁴)': None,
                'Wy,el (mm³)': None,
                'Wy,pl (mm³)': None,
                'iy (mm)': None,
                'Sy (mm³)': None,
                
                # Section properties - Axis z
                'Iz (mm⁴)': None,
                'Wz,el (mm³)': None,
                'Wz,pl (mm³)': None,
                'iz (mm)': None,
                'Sz (mm³)': None,
                
                # Warping and buckling
                'It (mm⁴)': None,
                'Ct (mm³)': None
            }
            
            # Kalınlık değerini hemen ata
            if thickness is not None:
                data['t (mm)'] = thickness
        elif profile_name.startswith('SHS'):
            parts = profile_name.split('x')
            thickness = float(parts[-1]) if len(parts) == 2 else None
            
            data = {
                'Profil': profile_name,
                'a (mm)': None,
                't (mm)': thickness,
                'r (mm)': None,
                'A (mm²)': None,
                'AL (m²/m)': None,
                'G (kg/m)': None,
                
                # Section properties
                'Iy (mm⁴)': None,
                'Wy (mm³)': None,
                'Wz (mm³)': None,
                'iy (mm)': None,
                'Iz (mm⁴)': None,
                'Wz (mm³)': None,
                'iz (mm)': None
            }
            
            # Kalınlık değerini hemen ata
            if thickness is not None:
                data['t (mm)'] = thickness
        elif profile_name.startswith('HEA'):
            data = {
                'Profil': profile_name,
                # Geometry
                'h (mm)': None,
                'b (mm)': None,
                'tw (mm)': None,
                'tf (mm)': None,
                'r1 (mm)': None,
                'r2 (mm)': None,
                'A (mm²)': None,
                'AL (m²/m)': None,
                'G (kg/m)': None,
                
                # Section properties
                'Iy (mm⁴)': None,
                'Wy1 (mm³)': None,
                'Wy,pl (mm³)': None,
                'iy (mm)': None,
                'Sy (mm³)': None,
                'Iz (mm⁴)': None,
                'Wz1 (mm³)': None,
                'Wz,pl (mm³)': None,
                'iz (mm)': None,
                'Sz (mm³)': None,
                
                # Warping and buckling
                'Iw (mm⁶)': None,
                'It (mm⁴)': None,  # Büyük I
                'ipc (mm)': None
            }
        else:
            # Diğer profiller için mevcut dictionary yapısı
            data = {
                'Profil': profile_name,
                # Geometry özellikleri
                'h (mm)': None, 'b (mm)': None, 'tw (mm)': None, 'tf (mm)': None,
                'r1 (mm)': None, 'r2 (mm)': None, 'ys (mm)': None, 'd (mm)': None,
                'AL (m²/m)': None, 'A (mm²)': None, 'G (kg/m)': None,
                't (mm)': None, 'ri (mm)': None, 'ro (mm)': None,
                
                # Section properties
                'Iy (mm⁴)': None, 'Wy1 (mm³)': None, 'Wy,pl (mm³)': None,
                'iy (mm)': None, 'Sy (mm³)': None, 'Iz (mm⁴)': None,
                'Wz1 (mm³)': None, 'Wz,pl (mm³)': None, 'iz (mm)': None,
                'Sz (mm³)': None, 'u (mm)': None, 'v (mm)': None,
                'u\' (°)': None, 'Iu (mm⁴)': None, 'Iv (mm⁴)': None,
                'iu (mm)': None, 'iv (mm)': None,
                
                # Warping and buckling
                'Iw (mm⁶)': None, 'iw (mm)': None, 'It (mm⁴)': None,
                'ipc (mm)': None
            }
        
        # RHS, SHS, CHS profilleri için kalınlık değerini al
        if profile_name.startswith(('RHS', 'SHS', 'CHS')):
            thickness = extract_thickness(profile_name)
            if thickness is not None:
                if profile_name.startswith('CHS'):
                    data['T (mm)'] = thickness
                else:
                    data['t (mm)'] = thickness
        
        # Her hücreyi kontrol et
        for cell in all_cells:
            try:
                text = cell.text.strip()
                
                # Debug: Tüm hücreleri yazdır
                print(f"Hücre içeriği: [{text}]")
                
                # Ct değeri için özel kontrol
                if 'Ct = ' in text:
                    data['Ct (mm³)'] = extract_value(text)
                    continue  # Ct işlendikten sonra diğer kontrollere geçme
                
                # It değeri için kontrol
                elif 'It = ' in text:
                    data['It (mm⁴)'] = extract_value(text)
                    continue  # It işlendikten sonra diğer kontrollere geçme
                
                # t veya T değeri için kontrol (CHS, RHS, SHS profilleri hariç)
                elif 't = ' in text and not profile_name.startswith(('RHS', 'SHS')):
                    data['t (mm)'] = extract_value(text)
                elif 'T = ' in text and not profile_name.startswith('CHS'):
                    data['T (mm)'] = extract_value(text)
                
                # Diğer kontroller aynı kalacak
                elif 'h = ' in text:
                    data['h (mm)'] = extract_value(text)
                elif 'b = ' in text:
                    data['b (mm)'] = extract_value(text)
                elif 'tw = ' in text:
                    data['tw (mm)'] = extract_value(text)
                elif 'tf = ' in text:
                    data['tf (mm)'] = extract_value(text)
                elif 'r1 = ' in text:
                    data['r1 (mm)'] = extract_value(text)
                elif 'r2 = ' in text:
                    data['r2 (mm)'] = extract_value(text)
                elif 'ys = ' in text:
                    data['ys (mm)'] = extract_value(text)
                elif 'd = ' in text:
                    data['d (mm)'] = extract_value(text)
                elif 'AL = ' in text:
                    data['AL (m²/m)'] = extract_value(text)
                elif 'A = ' in text:
                    data['A (mm²)'] = extract_value(text)
                elif 'G = ' in text:
                    data['G (kg/m)'] = extract_value(text)
                elif 't = ' in text:
                    data['t (mm)'] = extract_value(text)
                elif 'ri = ' in text:
                    data['ri (mm)'] = extract_value(text)
                elif 'ro = ' in text:
                    data['ro (mm)'] = extract_value(text)
                
                # Section properties
                elif 'Iy = ' in text:
                    data['Iy (mm⁴)'] = extract_value(text)
                elif 'Wy1 = ' in text:
                    data['Wy1 (mm³)'] = extract_value(text)
                elif 'Wy,pl = ' in text:
                    data['Wy,pl (mm³)'] = extract_value(text)
                elif 'iy = ' in text:
                    data['iy (mm)'] = extract_value(text)
                elif 'Sy = ' in text:
                    data['Sy (mm³)'] = extract_value(text)
                elif 'Iz = ' in text:
                    data['Iz (mm⁴)'] = extract_value(text)
                elif 'Wz1 = ' in text:
                    data['Wz1 (mm³)'] = extract_value(text)
                elif 'Wz,pl = ' in text:
                    data['Wz,pl (mm³)'] = extract_value(text)
                elif 'iz = ' in text:
                    data['iz (mm)'] = extract_value(text)
                elif 'Sz = ' in text:
                    data['Sz (mm³)'] = extract_value(text)
                elif 'u = ' in text:
                    data['u (mm)'] = extract_value(text)
                elif 'v = ' in text:
                    data['v (mm)'] = extract_value(text)
                elif 'u\' = ' in text:
                    data['u\' (°)'] = extract_value(text)
                elif 'Iu = ' in text:
                    data['Iu (mm⁴)'] = extract_value(text)
                elif 'Iv = ' in text:
                    data['Iv (mm⁴)'] = extract_value(text)
                elif 'iu = ' in text:
                    data['iu (mm)'] = extract_value(text)
                elif 'iv = ' in text:
                    data['iv (mm)'] = extract_value(text)
                
                # Warping and buckling
                elif 'Iw = ' in text:
                    data['Iw (mm⁶)'] = extract_value(text)
                elif 'iw = ' in text:
                    data['iw (mm)'] = extract_value(text)
                elif 'ipc = ' in text or 'IPC = ' in text:
                    print("\n=== ipc Değeri İşleniyor ===")
                    print(f"Bulunan metin: {text}")
                    try:
                        raw_value = text.split('=')[1].strip().split()[0]
                        print(f"Ham değer: {raw_value}")
                        
                        if 'E+' in raw_value:
                            base, exp = raw_value.split('E+')
                            base = float(base.replace(',', '.'))
                            exp = int(exp)
                            final_value = base * (10 ** exp)
                        else:
                            final_value = float(raw_value.replace(',', '.'))
                        
                        print(f"Hesaplanan değer: {final_value}")
                        data['ipc (mm)'] = final_value
                        print(f"Dictionary'de ipc değeri: {data['ipc (mm)']}")
                        
                    except Exception as e:
                        print(f"ipc değeri işlenirken hata: {str(e)}")
                
                # L profilleri için özel kontroller
                if profile_name.startswith('L'):
                    if 'b = ' in text:
                        data['b (mm)'] = extract_value(text)
                    elif 't = ' in text:
                        data['t (mm)'] = extract_value(text)
                    elif 'r1 = ' in text:
                        data['r1 (mm)'] = extract_value(text)
                    elif 'r2 = ' in text:
                        data['r2 (mm)'] = extract_value(text)
                    elif 'ys = ' in text:
                        data['ys (mm)'] = extract_value(text)
                    elif "y's = " in text:
                        data["y's (mm)"] = extract_value(text)
                    elif 'v = ' in text:
                        data['v (mm)'] = extract_value(text)
                    elif 'u1 = ' in text:
                        data['u1 (mm)'] = extract_value(text)
                    elif 'u2 = ' in text:
                        data['u2 (mm)'] = extract_value(text)
                    elif 'A = ' in text:
                        data['A (mm²)'] = extract_value(text)
                    elif 'AL = ' in text:
                        data['AL (m²/m)'] = extract_value(text)
                    elif 'G = ' in text:
                        data['G (kg/m)'] = extract_value(text)
                    
                    # Section properties - Axis y
                    elif 'Iy = ' in text:
                        data['Iy (mm⁴)'] = extract_value(text)
                    elif 'Wy1 = ' in text:
                        data['Wy1 (mm³)'] = extract_value(text)
                    elif 'Wy2 = ' in text:
                        data['Wy2 (mm³)'] = extract_value(text)
                    elif 'iy = ' in text:
                        data['iy (mm)'] = extract_value(text)
                    
                    # Section properties - Axis z
                    elif 'Iz = ' in text:
                        data['Iz (mm⁴)'] = extract_value(text)
                    elif 'Wz2 = ' in text:
                        data['Wz2 (mm³)'] = extract_value(text)
                    elif 'Wz3 = ' in text:
                        data['Wz3 (mm³)'] = extract_value(text)
                    elif 'iz = ' in text:
                        data['iz (mm)'] = extract_value(text)
                    
                    # Section properties - Main axes
                    elif 'Iu = ' in text:
                        data['Iu (mm⁴)'] = extract_value(text)
                    elif 'Iv = ' in text:
                        data['Iv (mm⁴)'] = extract_value(text)
                    elif 'Wu1 = ' in text:
                        data['Wu1 (mm³)'] = extract_value(text)
                    elif 'Wv2 = ' in text:
                        data['Wv2 (mm³)'] = extract_value(text)
                    elif 'Wv3 = ' in text:
                        data['Wv3 (mm³)'] = extract_value(text)
                    elif 'iu = ' in text:
                        data['iu (mm)'] = extract_value(text)
                    elif 'iv = ' in text:
                        data['iv (mm)'] = extract_value(text)
                    elif 'um = ' in text:
                        data['um (mm)'] = extract_value(text)
                    
                    # Warping and buckling
                    elif 'It = ' in text:
                        data['It (mm⁴)'] = extract_value(text)
                    elif 'ipc = ' in text:
                        data['ipc (mm)'] = extract_value(text)
                    elif 'ipa = ' in text:
                        data['ipa (mm)'] = extract_value(text)
                    elif 'Iyz = ' in text:
                        data['Iyz (mm⁴)'] = extract_value(text)
                    
                    continue  # L profilleri için kontrollerden sonra diğer kontrollere geçme
                
                # HEA profilleri için özel kontroller
                if profile_name.startswith('HEA'):
                    if 'h = ' in text:
                        data['h (mm)'] = extract_value(text)
                    elif 'b = ' in text:
                        data['b (mm)'] = extract_value(text)
                    elif 'tw = ' in text:
                        data['tw (mm)'] = extract_value(text)
                    elif 'tf = ' in text:
                        data['tf (mm)'] = extract_value(text)
                    elif 'r1 = ' in text:
                        data['r1 (mm)'] = extract_value(text)
                    elif 'r2 = ' in text:
                        data['r2 (mm)'] = extract_value(text)
                    elif 'A = ' in text:
                        data['A (mm²)'] = extract_value(text)
                    elif 'AL = ' in text:
                        data['AL (m²/m)'] = extract_value(text)
                    elif 'G = ' in text:
                        data['G (kg/m)'] = extract_value(text)
                    
                    # Section properties
                    elif 'Iy = ' in text:
                        data['Iy (mm⁴)'] = extract_value(text)
                    elif 'Wy1 = ' in text:
                        data['Wy1 (mm³)'] = extract_value(text)
                    elif 'Wy,pl = ' in text:
                        data['Wy,pl (mm³)'] = extract_value(text)
                    elif 'iy = ' in text:
                        data['iy (mm)'] = extract_value(text)
                    elif 'Sy = ' in text:
                        data['Sy (mm³)'] = extract_value(text)
                    elif 'Iz = ' in text:
                        data['Iz (mm⁴)'] = extract_value(text)
                    elif 'Wz1 = ' in text:
                        data['Wz1 (mm³)'] = extract_value(text)
                    elif 'Wz,pl = ' in text:
                        data['Wz,pl (mm³)'] = extract_value(text)
                    elif 'iz = ' in text:
                        data['iz (mm)'] = extract_value(text)
                    elif 'Sz = ' in text:
                        data['Sz (mm³)'] = extract_value(text)
                    
                    # Warping and buckling
                    elif 'Iw = ' in text:
                        data['Iw (mm⁶)'] = extract_value(text)
                    elif 'It = ' in text:  # Büyük I
                        data['It (mm⁴)'] = extract_value(text)
                    elif 'ipc = ' in text:
                        data['ipc (mm)'] = extract_value(text)
                    
                    continue  # HEA profilleri için kontrollerden sonra diğer kontrollere geçme
                
            except Exception as e:
                print(f"HATA: {str(e)}")
                print(f"Hata türü: {type(e)}")
                continue
        
        print("\nFonksiyon sonunda dictionary kontrolü:")
        for key, value in data.items():
            if value is not None:
                print(f"{key}: {value}")
        
        return data
        
    finally:
        if driver:
            driver.quit()

def get_profile_url(profile_name):
    """Profil adına göre URL oluşturur"""
    base_url = "https://www.staticstools.eu/en"
    
    # Profil tipini ve boyutunu ayır
    if profile_name.startswith('LU'):
        # LU profilleri için özel format
        # Örnek: LU30x30x4 -> L+30x30x4
        dimensions = profile_name[2:]  # "LU30x30x4" -> "30x30x4"
        return f"{base_url}/profile-lu/L+{dimensions}/mm/show"  # LU+ yerine L+ kullanıyoruz
    elif profile_name.startswith('HE'):
        return f"{base_url}/profile-he/{profile_name}/mm/show"
    elif profile_name.startswith('IPE'):
        return f"{base_url}/profile-ipe/{profile_name}/mm/show"
    elif profile_name.startswith('IPN'):
        return f"{base_url}/profile-ipn/{profile_name}/mm/show"
    elif profile_name.startswith('UPE'):
        return f"{base_url}/profile-upe/{profile_name}/mm/show"
    elif profile_name.startswith('UPN'):
        return f"{base_url}/profile-upn/{profile_name}/mm/show"
    else:
        raise ValueError(f"Desteklenmeyen profil tipi: {profile_name}")

def main():
    """Ana program"""
    profiles = {
        'HEA': ['HE100A', 'HE120A'],
        'RHS': ['RHS50x30x2.6'],
        'SHS': ['SHS40x2.6'],
        'CHS': ['CHS21.3x2.3'],
        'L': ['L20x20x3'],
        'T': ['T30']
    }
    
    all_results = []
    
    for profile_type, profile_list in profiles.items():
        print(f"\n{profile_type} profilleri işleniyor...")
        
        for profile in profile_list:
            print(f"\n{profile} profili için veri çekiliyor...")
            
            data = get_profile_data(profile)
            
            if data:
                all_results.append(data)
                print(f"Başarılı: {profile}")
            else:
                print(f"Başarısız: {profile}")
            
            time.sleep(2)
    
    if all_results:
        # Önce tüm olası sütunları belirle
        all_columns = set()
        for result in all_results:
            all_columns.update(result.keys())
        
        # DataFrame oluştur
        df = pd.DataFrame(all_results)
        
        # Sütunları düzenle - tüm sütunları dahil et
        columns = sorted(list(all_columns))  # Tüm sütunları alfabetik sırala
        
        # 'Profil' sütununu en başa al
        if 'Profil' in columns:
            columns.remove('Profil')
            columns = ['Profil'] + columns
        
        # DataFrame'i yeniden düzenle
        df = df.reindex(columns=columns)
        
        # Excel'e kaydet
        excel_file = "profil_verileri.xlsx"
        df.to_excel(excel_file, index=False)
        
        print(f"\nToplam {len(all_results)} profil verisi işlendi")
        print(f"Veriler kaydedildi: {excel_file}")
        print("\nKaydedilen sütunlar:")
        for col in df.columns:
            print(f"- {col}")
    else:
        print("\nHiç veri toplanamadı!")

if __name__ == "__main__":
    main() 