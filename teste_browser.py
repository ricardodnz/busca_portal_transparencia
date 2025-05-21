from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
# Modo visível para ver o que ocorre
# options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1200x800")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    driver.get("https://www.google.com")
    print("✅ Chrome abriu com sucesso.")
    print("Título da página:", driver.title)
    time.sleep(5)  # espera para você ver a janela
finally:
    driver.quit()
