from browser import iniciar_browser
from utils import salvar_json, capturar_tela_base64
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ✅ Função para fechar ou esconder o aviso de cookies e rodapé
def fechar_aviso_cookies(driver):
    try:
        modal = driver.find_element(By.ID, "cookiebar-modal")
        if modal.is_displayed():
            print("🟠 Fechando modal de cookies...")
            botao_fechar = modal.find_element(By.CSS_SELECTOR, ".br-button.primary")
            botao_fechar.click()
            WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.ID, "cookiebar-modal")))
    except:
        pass

    try:
        driver.execute_script("""
            const footer = document.getElementById('cookiebar-modal-footer');
            if (footer) {
                footer.style.display = 'none';
                footer.style.visibility = 'hidden';
                footer.style.height = '0px';
                footer.style.pointerEvents = 'none';
            }
        """)
        time.sleep(0.5)
    except:
        pass

# ✅ Função principal de execução do robô
def buscar_dados(driver, entrada):
    url = "https://portaldatransparencia.gov.br/pessoa/visao-geral"
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    try:
        print("🟡 Etapa 1: Clicando em 'Acessar busca'")
        fechar_aviso_cookies(driver)
        botao_acessar = wait.until(
            EC.element_to_be_clickable((By.ID, "button-consulta-pessoa-fisica"))
        )
        botao_acessar.click()

        print("🟡 Etapa 2: Clicando em 'Refine a busca'")
        fechar_aviso_cookies(driver)
        botao_refinar = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-controls='box-busca-refinada']"))
        )
        botao_refinar.click()

        print("🟡 Etapa 3: Marcando 'Beneficiário de Programa Social'")
        fechar_aviso_cookies(driver)
        print("🟡 Aguardando caixa 'Beneficiário de Programa Social' aparecer")
        checkbox = wait.until(EC.presence_of_element_located((By.ID, "beneficiarioProgramaSocial")))

        print("🟠 Rolando até o checkbox")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)

        # ✅ Tentativas de clique com validação
        tentativas = 0
        while tentativas < 5:
            try:
                print(f"🟡 Tentando marcar checkbox (tentativa {tentativas + 1})")
                checkbox = wait.until(EC.element_to_be_clickable((By.ID, "beneficiarioProgramaSocial")))
                checkbox.click()
                time.sleep(0.5)
                if checkbox.is_selected():
                    print("✅ Checkbox marcado com sucesso.")
                    break
            except Exception as e:
                print(f"⚠️ Tentativa falhou: {type(e).__name__}")
            tentativas += 1

        if not checkbox.is_selected():
            raise Exception("❌ Falha ao marcar o checkbox mesmo após 5 tentativas.")

        print("🟡 Etapa 4: Capturando tela")
        imagem_base64 = capturar_tela_base64(driver)

        print("🟡 Etapa 5: Clicando em 'Consultar'")
        fechar_aviso_cookies(driver)
        botao_consultar = wait.until(
            EC.element_to_be_clickable((By.ID, "btnConsultarPF"))
        )
        botao_consultar.click()

        print("🟢 Etapa 6: Aguardando resultados")
        resultados_div = wait.until(
            EC.presence_of_element_located((By.ID, "resultados"))
        )

        time.sleep(1)

        print("🟢 Etapa 7: Extraindo dados dos beneficiários")
        linhas = resultados_div.find_elements(By.CSS_SELECTOR, "ul > li")
        beneficiarios = []
        for linha in linhas[:10]:
            try:
                nome = linha.find_element(By.CSS_SELECTOR, ".col-dados .nome").text.strip()
                info = linha.find_element(By.CSS_SELECTOR, ".col-dados .detalhes").text.strip()
                beneficiarios.append({
                    "nome": nome,
                    "detalhes": info
                })
            except Exception:
                continue

        print("✅ Consulta concluída com sucesso.")
        return {
            "filtro_aplicado": "Beneficiário de Programa Social",
            "imagem_base64": imagem_base64,
            "beneficiarios": beneficiarios
        }

    except Exception as e:
        print(f"❌ Erro durante execução: {type(e).__name__}: {str(e)}")
        return {"erro": f"{type(e).__name__}: {str(e)}"}
