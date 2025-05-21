
# 🤖 RPA - Consulta de Beneficiários no Portal da Transparência

Este projeto em **Python** automatiza a consulta de **beneficiários de programas sociais** no Portal da Transparência do Governo Federal, realizando:

- ✔️ Navegação completa até o filtro por **"Beneficiário de Programa Social"**.
- ✔️ Captura de tela da busca no formato **Base64**.
- ✔️ Extração da lista de beneficiários retornada na busca.
- ✔️ Geração de saída em **JSON**, **Excel (.xlsx)** e **arquivo de texto (.txt)** com os dados e evidências.

---

## 📂 Estrutura do Projeto

```
rpa_transparencia/
├── main.py              # Script principal para executar o robô
├── browser.py           # Configuração do navegador (Selenium + Chrome)
├── scraper.py           # Lógica de navegação, scraping e extração dos dados
├── utils.py             # Funções auxiliares: salvar JSON, TXT e capturar tela em Base64
├── requirements.txt     # Lista de dependências Python
├── output/              # Resultados gerados (JSON, TXT, XLSX e capturas)
└── logs/                # Arquivos de log da execução
```

---

## ▶️ Como Executar

### 1️⃣ Instale as dependências

Execute no terminal ou prompt:

```bash
pip install -r requirements.txt
```

### 2️⃣ Execute o script principal

```bash
python main.py
```

O robô irá abrir o navegador (modo visível ou headless), realizar a busca no Portal da Transparência e gerar os arquivos de saída na pasta `/output`.

---

## 📤 Saída Gerada

Os arquivos são salvos na pasta `output/`:

- ✅ `saida_YYYYMMDD_HHMMSS.json` → Dados da consulta + imagem da tela em Base64.
- ✅ `beneficiarios_YYYYMMDD_HHMMSS.xlsx` → Planilha com os dados dos beneficiários.
- ✅ `beneficiarios_YYYYMMDD_HHMMSS.txt` → Arquivo texto com os dados formatados.
- ✅ Captura da tela (inserida no JSON em formato Base64).

### 🗂️ Exemplo de conteúdo JSON:

```json
{
  "filtro_aplicado": "Beneficiário de Programa Social",
  "imagem_base64": "iVBORw0KGgoAAAANSUhEUgAAA...",
  "beneficiarios": [
    {
      "nome": "MARIA SILVA",
      "cpf": "***.123.456-**",
      "detalhe": "Beneficiário de Programa Social"
    }
  ]
}
```

---

## 🧰 Requisitos

- ✅ Python 3.8 ou superior
- ✅ Google Chrome instalado
- ✅ Conexão ativa com a internet
- ✅ Sistema operacional Windows, Linux ou macOS

---

## 🚀 Funcionalidades

- 🔹 Executa em modo **visível ou headless**.
- 🔹 Fecha pop-ups de cookies automaticamente.
- 🔹 Garante logs detalhados da execução na pasta `/logs`.
- 🔹 Captura da tela como evidência (em Base64 no JSON).
- 🔹 Gera dados no formato estruturado: **JSON**, **XLSX** e **TXT**.

---

## ⚠️ Observações Importantes

- ✔️ Este projeto foi desenvolvido para fins **educacionais e demonstrativos**.
- ✔️ O uso desta automação deve respeitar os **termos de uso do Portal da Transparência**.
- ✔️ Sujeito a mudanças na estrutura do site. Caso o layout do Portal da Transparência mude, a automação poderá necessitar de ajustes nos seletores.

---

## ✨ Autor

**Ricardo Diniz** – RPA Python Developer  
🔗 [LinkedIn](https://www.linkedin.com) (adicione seu link)  
📧 Contato profissional: (adicione seu email, opcional)

---

## 📝 Licença

Este projeto está licenciado sob a **Licença MIT**. Consulte o arquivo `LICENSE` para mais informações.

---

## 🌟 Contribuição

Contribuições, melhorias e sugestões são bem-vindas!  
Basta abrir uma issue ou enviar um pull request. 🚀
# busca_portal_transparencia
