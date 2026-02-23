import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

print("MARKET DATA SCRAPER STARTED")
print("\n" + "-" * 50)

# Set standard headers to mimic a real browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 '
                  'Safari/537.36 '
}


# Helper Function: Save Files & Images
def save_scraped_data(source_name, response_text, soup, base_url):
    base_dir = f"outputs/{source_name}"
    images_dir = os.path.join(base_dir, 'images')

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    # 1. Save Raw HTML
    raw_path = os.path.join(base_dir, 'raw_page.html')
    with open(raw_path, 'w', encoding='utf-8') as f:
        f.write(response_text)
    print(f" + Raw HTML successfully saved to'{raw_path}'")

    # 2. Extract and Download Images
    img_tags = soup.find_all('img')
    downloaded_count = 0
    for img in img_tags:
        img_url = img.get('src') or img.get('data-src')
        if img_url:
            img_url = urljoin(base_url, img_url)
            try:
                if downloaded_count >= 3:
                    break

                # check image format
                if img_url.startswith('http') and any(
                        ext in img_url.lower() for ext in ['.jpg', '.png', '.jpeg', '.webp']):
                    img_data = requests.get(img_url, timeout=5).content
                    img_name = f"image_{downloaded_count + 1}.jpg"
                    img_path = os.path.join(images_dir, img_name)

                    with open(img_path, 'wb') as handler:
                        handler.write(img_data)
                    downloaded_count += 1
            except Exception:
                pass

    print(f" + {downloaded_count} Images successfully downloaded to '{images_dir}'")

    # 3. Clean HTML (remove scripts and styles)
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()

    clean_path = os.path.join(base_dir, 'clean_page.html')
    with open(clean_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f" + Clean HTML successfully saved to '{clean_path}'")

    # 4. Save Pure Text
    text_path = os.path.join(base_dir, 'pure_text.txt')
    text_content = soup.get_text(separator='\n', strip=True)
    with open(text_path, 'w', encoding='utf-8') as f:
        f.write(text_content)
    print(f" + Pure text successfully saved to '{text_path}'")


# 1. SCRAPE GOLD PRICE
print("* Fetching Gold data from tgju.org...")
url_gold = 'https://www.tgju.org/profile/geram18'

try:
    response_gold = requests.get(url_gold, headers=headers)
    if response_gold.status_code == 200:
        soup_gold = BeautifulSoup(response_gold.text, 'html.parser')

        # Extract 18K Gold Price
        gold_element = soup_gold.find('span', attrs={'data-col': 'info.last_trade.PDrCotVal'})
        if gold_element:
            gold_price = gold_element.text.strip()
            print(f"   ✅ Extracted Price (18K Gold): {gold_price} IRR")
        else:
            print("❌    Gold price element not found!")

        # Save Files
        save_scraped_data("gold", response_gold.text, soup_gold, url_gold)
    else:
        print(f"   ❌ Error fetching Gold data. Status: {response_gold.status_code}")
except Exception as e:
    print(f"   ❌ Exception in Gold scraper: {e}")

print("-" * 50)

# 2. SCRAPE OIL PRICE
print("* Fetching Oil data from oilprice.com...")
url_oil = 'https://oilprice.com/'

try:
    response_oil = requests.get(url_oil, headers=headers)
    if response_oil.status_code == 200:
        soup_oil = BeautifulSoup(response_oil.text, 'html.parser')

        # Extract Brent Crude Price
        brent_row = soup_oil.find('tr', attrs={'data-hash': 'Brent-Crude'})
        if brent_row:
            oil_element = brent_row.find('td', class_='value')
            if oil_element:
                oil_price = oil_element.get_text(strip=True)
                print(f"   ✅ Extracted Price (Brent Crude): ${oil_price} USD")
            else:
                print("❌    Oil price value column not found!")
        else:
            print("❌    Brent Crude row not found!")

        # Save Files
        save_scraped_data("oil", response_oil.text, soup_oil, url_oil)
    else:
        print(f"   ❌ Error fetching Oil data. Status: {response_oil.status_code}")
except Exception as e:
    print(f"   ❌ Exception in Oil scraper: {e}")

print("\n" + "-" * 50)
print("SCRAPING PROCESS COMPLETED")