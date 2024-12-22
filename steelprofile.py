from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# WebDriver başlat
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Hedef URL
url = "https://www.staticstools.eu/en"
driver.get(url)

try:
    # 'Select' öğesini bul
    select_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, "profile"))
    )
    select = Select(select_element)

    # Profillerin bilgilerini saklamak için bir liste
    profiles_data = []

    # Tüm seçenekleri döngüyle işle
    for index, option in enumerate(select.options):
        value = option.get_attribute("value")
        text = option.text.strip()
        print(f"Profil işleniyor: {text}")

        # Profil seçimi
        try:
            select.select_by_value(value)

            # Formun otomatik gönderilmesini bekle
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "table"))
            )

            # Tabloyu bul ve satırları oku
            table = driver.find_element(By.CLASS_NAME, "table")
            rows = table.find_elements(By.TAG_NAME, "tr")

            # Profil özelliklerini kaydetmek için bir sözlük
            profile_details = {"Profil Adı": text}

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) == 2:  # Sadece iki sütunlu satırları işle
                    property_name = cells[0].text.strip()
                    property_value = cells[1].text.strip()
                    profile_details[property_name] = property_value

            # Profili listeye ekle
            profiles_data.append(profile_details)

        except Exception as e:
            print(f"Profil işlenirken hata oluştu ({text}): {e}")

        # Ana sayfaya dön
        driver.get(url)

        # 'Select' öğesini yeniden bul (çünkü sayfa yenilendi)
        select_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, "profile"))
        )
        select = Select(select_element)

        # Her 10 profilden sonra WebDriver'ı yeniden başlat
        if index > 0 and index % 10 == 0:
            print("WebDriver yeniden başlatılıyor...")
            driver.quit()
            driver = webdriver.Chrome(service=service, options=options)
            driver.get(url)

    # Verileri pandas DataFrame'e dönüştür
    df = pd.DataFrame(profiles_data)

    # Excel dosyasına yaz
    output_file = "profiller_ozellikler.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Veriler {output_file} dosyasına başarıyla aktarıldı.")

except Exception as e:
    print(f"Hata oluştu: {e}")

finally:
    driver.quit()