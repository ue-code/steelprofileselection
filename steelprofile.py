from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import pandas as pd
import time

# WebDriver ayarları
driver = webdriver.Chrome()
driver.maximize_window()

# Hedef URL
base_url = "https://www.staticstools.eu/en"
driver.get(base_url)

try:
    # Profil bağlantılarını bul
    profile_links = [
        link.get_attribute("href")
        for link in driver.find_elements(By.CSS_SELECTOR, "a[href*='/profile-']")
        if "/en/profile-" in link.get_attribute("href")
    ]
    profile_links = list(set(profile_links))  # Tekrar edenleri kaldır
    print(f"{len(profile_links)} adet profil bağlantısı bulundu.")

    # Profil verilerini saklamak için liste
    profiles_data = []

    # Her profil bağlantısını işle
    for profile_url in profile_links:
        profile_type = profile_url.split("/profile-")[1].split("/")[0].upper()
        print(f"Profil tipi işleniyor: {profile_type}")

        driver.get(profile_url)
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        try:
            select_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "profile"))
            )
            select = Select(select_element)
            options = [opt for opt in select.options if opt.get_attribute("value")]

            for option in options:
                value = option.get_attribute("value")
                text = option.text.strip()

                if text.lower() == "select section" or not value:
                    continue

                print(f"Seçenek işleniyor: {text}")

                # URL'yi oluştur ve sayfayı aç
                section_url = f"{profile_url}/{value}/mm/show"
                driver.get(section_url)

                try:
                    WebDriverWait(driver, 10).until(
                        lambda d: d.execute_script("return document.readyState") == "complete"
                    )

                    # Tabloyu bul ve verileri oku
                    table = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "table"))
                    )
                    rows = table.find_elements(By.TAG_NAME, "tr")

                    for row in rows:
                        cells = row.find_elements(By.TAG_NAME, "td")
                        if len(cells) == 2:
                            property_name = cells[0].text.strip()
                            property_value = cells[1].text.strip()

                            profile_data = {
                                "Profil Tipi": profile_type,
                                "Kesit Boyutu": text,
                                "Özellik": property_name,
                                "Değer": property_value,
                                "URL": section_url,
                            }
                            profiles_data.append(profile_data)

                except (StaleElementReferenceException, TimeoutException) as e:
                    print(f"Tablo işlenirken hata oluştu ({text}): {e}")
                    continue

        except (StaleElementReferenceException, TimeoutException) as e:
            print(f"Profil işlenirken hata oluştu ({profile_type}): {e}")
            continue

    # Verileri pandas DataFrame'e dönüştür
    df = pd.DataFrame(profiles_data)

    # Excel dosyasına yaz
    output_file = "tum_profiller.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Veriler {output_file} dosyasına başarıyla aktarıldı.")

except Exception as e:
    print(f"Hata oluştu: {e}")

finally:
    driver.quit()