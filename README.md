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

- Kesit özellikleri çekilmek istenen her profil için kod bloğunda ilgili yere, profilin adı yazılmalıdır.

## Özellikler

- **Geometri**: Profilin boyutları ve ağırlık merkezi gibi geometrik özellikler.
- **Kesit Özellikleri**: Atalet momentleri, mukavemet momentleri ve atalet yarıçapları.
- **Burulma ve Çarpılma**: Burulma ve çarpılma ile ilgili özellikler.

## Notlar

- Her profil tipi için farklı özellikler mevcuttur. Kod, her profil tipi için uygun özellikleri çeker ve kaydeder.


## Katkıda Bulunma

Katkıda bulunmak isterseniz, lütfen bir pull request gönderin veya bir sorun bildirin.

## Lisans

- Bu proje MIT Lisansı ile lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın.

----

This project automatically retrieves section properties for various types of steel profiles and saves them to an Excel file. 
The project collects data from web pages using Selenium and processes the data with pandas.

## Requirements

- Python 3.x
- Selenium
- pandas
- openpyxl
- webdriver_manager

## Installation

Install the necessary Python packages.
Install Chrome WebDriver. The webdriver_manager package will automatically manage the WebDriver.

## Usage

1. Run `steelprofileselection.py`:

   ```bash
   python steelprofileselection.py
   ```
2. The program fetches data for the specified steel profiles and saves it to an Excel file named  `profil_verileri.xlsx`.
3. You can add the required profiles for data extraction to the relevant section of the code block.
   
## Features

- **Geometry** : Geometric properties such as the dimensions of the profile and the center of gravity.
- **Section Properties**: Moments of inertia, section moduli, and radii of gyration.
- **Torsion and Bending**: Properties related to torsion and bending.
  
## Notes

- Different properties are available for each profile type. The code retrieves and saves the appropriate properties for each profile type.
  
## Contributing

- If you would like to contribute, please submit a pull request or report an issue.

## License

- This project is licensed under the MIT License. For more information, see the `LICENSE` file.


