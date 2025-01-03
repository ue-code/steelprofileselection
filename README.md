# Steel Profile Selection

Bu proje, çeşitli çelik profil tipleri için kesit özelliklerini otomatik olarak çekip Excel dosyasına kaydeder. Proje, Selenium kullanarak web sayfalarından veri toplar ve pandas ile verileri işler.

## Gereksinimler

- Python 3.x
- Selenium
- pandas
- openpyxl
- webdriver_manager

## Kurulum

1. Gerekli Python paketlerini yükleyin:

   ```bash
   pip install selenium pandas openpyxl webdriver_manager
   ```

2. Chrome WebDriver'ı kurun. `webdriver_manager` paketi, WebDriver'ı otomatik olarak yönetecektir.

## Kullanım

1. `steelprofileselection.py` dosyasını çalıştırın:

   ```bash
   python steelprofileselection.py
   ```

2. Program, belirtilen çelik profiller için verileri çeker ve `profil_verileri.xlsx` adlı bir Excel dosyasına kaydeder.

## Desteklenen Profil Tipleri

- HEA
- RHS
- SHS
- CHS
- L
- T

## Özellikler

- **Geometri**: Profilin boyutları ve ağırlık merkezi gibi geometrik özellikler.
- **Kesit Özellikleri**: Atalet momentleri, mukavemet momentleri ve atalet yarıçapları.
- **Burulma ve Çarpılma**: Burulma ve çarpılma ile ilgili özellikler.

## Notlar

- Her profil tipi için farklı özellikler mevcuttur. Kod, her profil tipi için uygun özellikleri çeker ve kaydeder.
- `It` ve `Ct` gibi özellikler, doğru sütunlara yazılır ve karışıklık önlenir.

## Katkıda Bulunma

Katkıda bulunmak isterseniz, lütfen bir pull request gönderin veya bir sorun bildirin.

## Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın.
