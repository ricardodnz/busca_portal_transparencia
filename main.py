from browser import iniciar_browser
from scraper import buscar_dados
from utils import salvar_json
from datetime import datetime


if __name__ == "__main__":
    print("🚀 Iniciando o robô...")

    entrada = {"nome": "MARIA", "cpf_nis": ""}
    driver = iniciar_browser()

    try:
        dados = buscar_dados(driver, entrada)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        salvar_json(dados, f"saida_{timestamp}.json")

        print(f"✅ Dados coletados e salvos no arquivo 'saida_{timestamp}.json'")

    except Exception as e:
        print(f"❌ Erro durante execução: {e}")

    finally:
        driver.quit()
        print("🛑 Navegador fechado. Robô finalizado.")
