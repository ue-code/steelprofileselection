from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def setup_driver():
    """Selenium WebDriver'ı yapılandır"""
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_profile_data(profile_name):
    """Belirli bir profil için verileri çeker"""
    driver = None
    
    def extract_value(text):
        """Metinden sayısal değeri çıkarır"""
        try:
            value_str = text.split('=')[1].strip().split()[0]
            if 'e+' in value_str.lower():
                # Bilimsel gösterim (örn: 7.77e+5)
                return float(value_str.replace(',', '.'))
            else:
                # Normal gösterim
                return float(value_str.replace(',', '.'))
        except:
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
        time.sleep(3)
        
        # Tüm tabloları bul
        wait = WebDriverWait(driver, 10)
        tables = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "table")))
        
        all_cells = []
        for table in tables:
            cells = table.find_elements(By.TAG_NAME, "td")
            all_cells.extend(cells)
            
        print(f"Toplam bulunan hücre sayısı: {len(all_cells)}")
        
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
            'ipc (mm)': None, 'Ip (mm⁴)': None
        }
        
        # Her hücreyi kontrol et
        for cell in all_cells:
            try:
                text = cell.text.strip()
                
                # Geometry özellikleri
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
                elif 'It = ' in text:
                    data['It (mm⁴)'] = extract_value(text)
                elif 'ipc = ' in text:
                    data['ipc (mm)'] = extract_value(text)
                elif 'Ip = ' in text:
                    data['Ip (mm⁴)'] = extract_value(text)
                
            except Exception as e:
                print(f"Hücre işleme hatası: {str(e)}")
                continue
        
        return data
        
    finally:
        if driver:
            driver.quit()

def main():
    """Ana program"""
    profiles = {
        'HEA': [
            'HE100A', 'HE120A', 'HE140A', 'HE160A', 'HE180A', 'HE200A', 'HE220A', 'HE240A', 
            'HE260A', 'HE280A', 'HE300A', 'HE320A', 'HE340A', 'HE360A', 'HE400A', 'HE450A', 
            'HE500A', 'HE550A', 'HE600A', 'HE650A', 'HE700A', 'HE800A', 'HE900A', 'HE1000A'
        ],
        'HEAA': [
            'HE100AA', 'HE120AA', 'HE140AA', 'HE160AA', 'HE180AA', 'HE200AA', 'HE220AA', 
            'HE240AA', 'HE260AA', 'HE280AA', 'HE300AA', 'HE320AA', 'HE340AA', 'HE360AA', 
            'HE400AA', 'HE450AA', 'HE500AA', 'HE550AA', 'HE600AA', 'HE650AA', 'HE700AA', 
            'HE800AA', 'HE900AA', 'HE1000AA'
        ],
        'HEB': [
            'HE100B', 'HE120B', 'HE140B', 'HE160B', 'HE180B', 'HE200B', 'HE220B', 'HE240B',
            'HE260B', 'HE280B', 'HE300B', 'HE320B', 'HE340B', 'HE360B', 'HE400B', 'HE450B',
            'HE500B', 'HE550B', 'HE600B', 'HE650B', 'HE700B', 'HE800B', 'HE900B', 'HE1000B'
        ],
        'HEM': [
            'HE100M', 'HE120M', 'HE140M', 'HE160M', 'HE180M', 'HE200M', 'HE220M', 'HE240M',
            'HE260M', 'HE280M', 'HE300M', 'HE320M', 'HE360M', 'HE400M', 'HE450M', 'HE500M',
            'HE550M', 'HE600M', 'HE650M', 'HE700M', 'HE800M', 'HE900M', 'HE1000M'
        ],
        'HD': [
            'HD260', 'HD320', 'HD400'
        ],
        'HL': [
            'HL920', 'HL1000'
        ],
        'IPE': [
            'IPE80', 'IPE100', 'IPE120', 'IPE140', 'IPE160', 'IPE180', 'IPE200', 'IPE220',
            'IPE240', 'IPE270', 'IPE300', 'IPE330', 'IPE360', 'IPE400', 'IPE450', 'IPE500',
            'IPE550', 'IPE600'
        ],
        'IPEA': [
            'IPEA100', 'IPEA120', 'IPEA140', 'IPEA160', 'IPEA180', 'IPEA200', 'IPEA220',
            'IPEA240', 'IPEA270', 'IPEA300', 'IPEA330', 'IPEA360', 'IPEA400', 'IPEA450',
            'IPEA500', 'IPEA550', 'IPEA600'
        ],
        'IPEAA': [
            'IPEAA100', 'IPEAA120', 'IPEAA140', 'IPEAA160', 'IPEAA180', 'IPEAA200', 'IPEAA220',
            'IPEAA240', 'IPEAA270', 'IPEAA300', 'IPEAA330', 'IPEAA360', 'IPEAA400', 'IPEAA450',
            'IPEAA500', 'IPEAA550', 'IPEAA600'
        ],
        'IPEO': [
            'IPEO180', 'IPEO200', 'IPEO220', 'IPEO240', 'IPEO270', 'IPEO300', 'IPEO330',
            'IPEO360', 'IPEO400', 'IPEO450', 'IPEO500', 'IPEO550', 'IPEO600'
        ],
        'IPN': [
            'IPN80', 'IPN100', 'IPN120', 'IPN140', 'IPN160', 'IPN180', 'IPN200', 'IPN220',
            'IPN240', 'IPN260', 'IPN280', 'IPN300', 'IPN320', 'IPN340', 'IPN360', 'IPN380',
            'IPN400', 'IPN450', 'IPN500', 'IPN550', 'IPN600'
        ],
        'UPN': [
            'UPN80', 'UPN100', 'UPN120', 'UPN140', 'UPN160', 'UPN180', 'UPN200', 'UPN220',
            'UPN240', 'UPN260', 'UPN280', 'UPN300', 'UPN320', 'UPN350', 'UPN380', 'UPN400'
        ],
        'UPE': [
            'UPE80', 'UPE100', 'UPE120', 'UPE140', 'UPE160', 'UPE180', 'UPE200', 'UPE220',
            'UPE240', 'UPE270', 'UPE300', 'UPE330', 'UPE360', 'UPE400'
        ],
        'UAP': [
            'UAP100', 'UAP130', 'UAP150', 'UAP175', 'UAP200', 'UAP220', 'UAP250', 'UAP300'
        ],
        'L': [  # Le profilleri
            'L20x20x3', 'L25x25x3', 'L30x30x3', 'L35x35x4', 'L40x40x4', 'L45x45x4.5',
            'L50x50x5', 'L60x60x6', 'L70x70x7', 'L80x80x8', 'L90x90x9', 'L100x100x10',
            'L120x120x11', 'L130x130x12', 'L150x150x14', 'L200x200x16'
        ],
        'LU': [  # Lu profilleri
            'LU30x30x4', 'LU40x40x5', 'LU50x50x6', 'LU60x60x7', 'LU70x70x8',
            'LU80x80x9', 'LU90x90x10', 'LU100x100x11'
        ],
        'T': [
            'T20x20x3', 'T25x25x3', 'T30x30x4', 'T40x40x5', 'T50x50x6', 'T60x60x7',
            'T70x70x8', 'T80x80x9', 'T100x100x11'
        ],
        'SHS': [  # Square Hollow Section
            'SHS40x40x3', 'SHS50x50x3', 'SHS60x60x3', 'SHS80x80x3', 'SHS100x100x3',
            'SHS120x120x3', 'SHS140x140x3', 'SHS160x160x3', 'SHS180x180x3', 'SHS200x200x3'
        ],
        'RHS': [  # Rectangular Hollow Section
            'RHS60x40x3', 'RHS80x40x3', 'RHS100x50x3', 'RHS120x60x3', 'RHS140x70x3',
            'RHS160x80x3', 'RHS180x100x3', 'RHS200x100x3'
        ],
        'CHS': [  # Circular Hollow Section
            'CHS42.4x3', 'CHS48.3x3', 'CHS60.3x3', 'CHS76.1x3', 'CHS88.9x3',
            'CHS114.3x3', 'CHS139.7x3', 'CHS168.3x3', 'CHS219.1x3'
        ]
    }
    
    all_results = []
    
    for profile_type, profile_list in profiles.items():
        print(f"\n{profile_type} profilleri işleniyor...")
        
        for profile in profile_list:
            print(f"\n{profile} profili için veri çekiliyor...")
            
            data = get_profile_data(profile)
            
            if data:
                data['Profil'] = profile
                all_results.append(data)
                print(f"Başarılı: {profile}")
            else:
                print(f"Başarısız: {profile}")
            
            time.sleep(2)
    
    if all_results:
        df = pd.DataFrame(all_results)
        
        # Sütun sırasını düzenle
        columns = [
            'Profil', 
            'h (mm)', 'b (mm)', 'tw (mm)', 'tf (mm)', 'r1 (mm)', 'r2 (mm)',
            'ys (mm)', 'd (mm)', 'AL (m²/m)', 'A (mm²)', 'G (kg/m)',
            'Iy (mm⁴)', 'Wy1 (mm³)', 'Wy,pl (mm³)', 'iy (mm)', 'Sy (mm³)',
            'Iz (mm⁴)', 'Wz1 (mm³)', 'Wz,pl (mm³)', 'iz (mm)', 'Sz (mm³)',
            'Iw (mm⁶)', 'iw (mm)', 'It (mm⁴)', 'ipc (mm)'
        ]
        df = df[columns]
        
        excel_file = "profil_verileri.xlsx"
        df.to_excel(excel_file, index=False, sheet_name='Profil Verileri')
        
        print(f"\nToplam {len(all_results)} profil verisi işlendi")
        print(f"Veriler kaydedildi: {excel_file}")
        
        print("\nDataFrame Özeti:")
        print(df.head())
        print("\nBoş değer kontrolü:")
        print(df.isnull().sum())
    else:
        print("\nHiç veri toplanamadı!")

if __name__ == "__main__":
    main() 