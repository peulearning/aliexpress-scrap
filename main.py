from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

def scrape_aliexpress_product(url):
    # Configurações para o Firefox
    firefox_options = Options()
    firefox_options.add_argument("--headless")  # Executa o Firefox em modo headless

    # Configura o serviço com o GeckoDriver
    service = Service('/usr/local/bin/geckodriver')
    try:
        driver = webdriver.Firefox(service=service, options=firefox_options)
    except Exception as e:
        print(f"Erro ao iniciar o GeckoDriver: {e}")
        return

    try:
        driver.get(url)
        print("Página carregada com sucesso.")

        # Espera até que a div com as informações do produto esteja presente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.pdp-info-right'))
        )
        print("Div com informações do produto encontrada.")

        # Extrai informações do produto
        try:
            # Título do produto
            title_element = driver.find_element(By.CSS_SELECTOR, 'div.title--wrap--UUHae_g h1')
            title = title_element.text

            # Preço do produto
            price_element = driver.find_element(By.CSS_SELECTOR, 'span.price--currentPriceText--V8_y_b5')
            price = price_element.text

            # Monta o JSON com os dados do produto
            product_info = {
                'title': title,
                'price': price
            }

            return json.dumps(product_info, indent=4, ensure_ascii=False)

        except Exception as e:
            print(f"Erro ao extrair informações do produto: {e}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

# URL do produto
url = 'https://pt.aliexpress.com/item/1005005973217434.html?spm=a2g0o.productlist.main.1.5892744eWysxdJ&algo_pvid=9f70f8ed-afff-4404-910e-75c2b808e815&algo_exp_id=9f70f8ed-afff-4404-910e-75c2b808e815-0&pdp_npi=4%40dis%21BRL%2155.44%214.99%21%21%2169.10%216.22%21%402101fb0b17241063315854714e4eda%2112000035119267179%21sea%21BR%210%21ABX&curPageLogUid=w6rwNhMvUc3O&utparam-url=scene%3Asearch%7Cquery_from%3A'
product_data = scrape_aliexpress_product(url)
print(product_data)
