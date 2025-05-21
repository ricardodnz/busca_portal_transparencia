from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def iniciar_browser(headless=True):
    chrome_options = Options()

    if headless:
        #chrome_options.add_argument("--headless=new")  # Novo headless mais estável
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--disable-3d-apis")
        chrome_options.add_argument("--use-gl=swiftshader")

    # ✅ Configurações comuns (headless ou não)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    # ✅ Silenciar logs de erro do Chrome
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--silent")

    # ✅ Inicialização do driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver
