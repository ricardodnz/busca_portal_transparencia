import json
import os
import base64


def salvar_json(dados, nome_arquivo):
    """
    Salva um dicionário em formato JSON na pasta 'output'.
    Cria a pasta se ela não existir.

    :param dados: Dicionário com os dados a serem salvos.
    :param nome_arquivo: Nome do arquivo (ex: 'saida_20240520.json').
    """
    os.makedirs("output", exist_ok=True)
    caminho = os.path.join("output", nome_arquivo)

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


def salvar_txt(conteudo, nome_arquivo):
    """
    Salva um conteúdo textual (string) em um arquivo .txt na pasta 'output'.
    Cria a pasta se ela não existir.

    :param conteudo: String com o conteúdo a ser salvo.
    :param nome_arquivo: Nome do arquivo (ex: 'beneficiarios.txt').
    """
    os.makedirs("output", exist_ok=True)
    caminho = os.path.join("output", nome_arquivo)

    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)


def capturar_tela_base64(driver):
    """
    Captura uma imagem da tela atual do navegador e retorna em base64.

    :param driver: Instância do navegador Selenium WebDriver.
    :return: String em base64 da imagem capturada.
    """
    screenshot = driver.get_screenshot_as_png()
    imagem_base64 = base64.b64encode(screenshot).decode('utf-8')
    return imagem_base64
