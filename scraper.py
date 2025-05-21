import os
import pandas as pd
import time
from datetime import datetime
from browser import iniciar_browser
from utils import salvar_json, capturar_tela_base64
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def fechar_aviso_cookies(driver, logs):
    try:
        modal = driver.find_element(By.ID, "cookiebar-modal")
        if modal.is_displayed():
            logs.append("🟠 Fechando modal de cookies...")
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


def buscar_dados(driver, entrada):
    logs = []
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    url = "https://portaldatransparencia.gov.br/pessoa/visao-geral"
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    try:
        logs.append("🟡 Etapa 1: Clicando em 'Acessar busca'")
        fechar_aviso_cookies(driver, logs)
        botao_acessar = wait.until(EC.element_to_be_clickable((By.ID, "button-consulta-pessoa-fisica")))
        botao_acessar.click()

        logs.append("🟡 Etapa 2: Clicando em 'Refine a busca'")
        fechar_aviso_cookies(driver, logs)
        botao_refinar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-controls='box-busca-refinada']")))
        botao_refinar.click()

        logs.append("🟠 Focando visualmente no título 'Refine a Busca'")
        span_refine = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.title")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'}); arguments[0].focus();", span_refine)
        time.sleep(1)

        logs.append("🟡 Etapa 3: Localizando checkbox e label")
        fechar_aviso_cookies(driver, logs)

        checkbox = wait.until(EC.presence_of_element_located((By.ID, "beneficiarioProgramaSocial")))
        label = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='beneficiarioProgramaSocial']")))

        logs.append("🟡 Tentando marcar o checkbox via clique no label")
        try:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'}); arguments[0].focus();", label)
            time.sleep(0.5)
            label.click()
            time.sleep(0.5)

            if checkbox.is_selected():
                logs.append("✅ Checkbox marcado com sucesso via label.")
            else:
                raise Exception("❌ Checkbox NÃO foi marcado mesmo após clique no label.")
        except Exception as e:
            logs.append(f"❌ Erro ao clicar no label: {type(e).__name__}: {e}")
            salvar_log_txt(logs, timestamp)
            return {"erro": f"{type(e).__name__}: {e}"}

        logs.append("🟡 Etapa 4: Capturando tela")
        imagem_base64 = capturar_tela_base64(driver)

        logs.append("🟡 Etapa 5: Clicando em 'Consultar'")
        fechar_aviso_cookies(driver, logs)
        botao_consultar = wait.until(EC.element_to_be_clickable((By.ID, "btnConsultarPF")))
        botao_consultar.click()

        logs.append("🟢 Etapa 6: Aguardando resultados")
        resultados_div = wait.until(EC.presence_of_element_located((By.ID, "resultados")))
        time.sleep(1)

        logs.append("🟢 Etapa 7: Extraindo dados dos beneficiários")
        linhas = resultados_div.find_elements(By.CSS_SELECTOR, "div.br-item")
        logs.append(f"🔍 Total de itens encontrados: {len(linhas)}")

        beneficiarios = []
        for linha in linhas:
            try:
                nome = linha.find_element(By.CSS_SELECTOR, "a.link-busca-nome").text.strip()
                cpf = linha.find_element(By.CSS_SELECTOR, "strong").text.strip()
                detalhe = linha.find_elements(By.CSS_SELECTOR, "div.col-sm-12")[-1].text.strip()

                beneficiarios.append({
                    "nome": nome,
                    "cpf": cpf,
                    "detalhe": detalhe
                })
            except Exception as e:
                logs.append(f"⚠️ Erro ao processar item: {type(e).__name__}: {e}")
                continue

        logs.append("✅ Consulta concluída com sucesso.")

        # Cria diretórios
        os.makedirs("output", exist_ok=True)
        os.makedirs("logs", exist_ok=True)

        # ✅ Salvar JSON
        dados_json = {
            "filtro_aplicado": "Beneficiário de Programa Social",
            "imagem_base64": imagem_base64,
            "beneficiarios": beneficiarios
        }
        salvar_json(dados_json, f"saida_{timestamp}.json")
        logs.append(f"📄 JSON salvo como 'output/saida_{timestamp}.json'")

        # ✅ Salvar como planilha
        try:
            df = pd.DataFrame(beneficiarios)
            df.to_excel(f"output/beneficiarios_{timestamp}.xlsx", index=False)
            logs.append(f"📄 Planilha salva em 'output/beneficiarios_{timestamp}.xlsx'")
        except Exception as e:
            logs.append(f"❌ Erro ao salvar planilha: {type(e).__name__}: {e}")

        # ✅ Salvar como .txt
        try:
            with open(f"output/beneficiarios_{timestamp}.txt", "w", encoding="utf-8") as f:
                for b in beneficiarios:
                    f.write(f"Nome: {b['nome']}\nCPF: {b['cpf']}\nDetalhes: {b['detalhe']}\n\n")
            logs.append(f"📄 Arquivo texto salvo em 'output/beneficiarios_{timestamp}.txt'")
        except Exception as e:
            logs.append(f"❌ Erro ao salvar TXT: {type(e).__name__}: {e}")

        salvar_log_txt(logs, timestamp)
        return dados_json

    except Exception as e:
        msg = f"❌ Erro durante execução: {type(e).__name__}: {str(e)}"
        logs.append(msg)
        salvar_log_txt(logs, timestamp)
        return {"erro": msg}


def salvar_log_txt(logs, timestamp):
    os.makedirs("logs", exist_ok=True)
    with open(f"logs/executar_log_{timestamp}.txt", "w", encoding="utf-8") as f:
        for linha in logs:
            f.write(linha + "\n")
