from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpC
import time,re

def extrair_dados(evento):
    titulo_bruto = evento["titulo"].replace('\u2009', ' ').replace('\n', ' ').strip()
    link = evento["link"]

    #Pega a data (dia e mês)
    data_match = re.match(r"(\d{1,2})\s+([A-Z]{3,4})\.", titulo_bruto)
    dia, mes = None, None
    if data_match:
        dia = int(data_match.group(1))
        mes_str = data_match.group(2)
        meses = {
            "JAN": 1, "FEV": 2, "MAR": 3, "ABR": 4, "MAI": 5, "JUN": 6,
            "JUL": 7, "AGO": 8, "SET": 9, "OUT": 10, "NOV": 11, "DEZ": 12
        }
        mes = meses.get(mes_str.upper(), 0)

    #Encontra a hora
    horario_match = re.search(r"\b(\d{1,2}:\d{2})\b", titulo_bruto)
    hora = horario_match.group(1) if horario_match else None

    #Obtem titulo
    titulo_evento_match = re.search(r"\.\s*(.*?)(?:\s+\w{3}\.|\s+\|\s+| no | em | - )", titulo_bruto)
    titulo_evento = titulo_evento_match.group(1).strip() if titulo_evento_match else "Título não identificado"

    #Explora cidade e estado
    cidade_estado_match = re.search(r"\s*([A-Za-zÀ-ÿ\s]+)\s*-\s*([A-Z]{2})\s*$", titulo_bruto)
    cidade = cidade_estado_match.group(1).strip() if cidade_estado_match else "Cidade não identificada"
    estado = cidade_estado_match.group(2) if cidade_estado_match else "Estado não identificado"

    estados = {
        "AC": "Acre", "AL": "Alagoas", "AM": "Amazonas", "AP": "Amapá", "BA": "Bahia", "CE": "Ceará",
        "DF": "Distrito Federal", "ES": "Espírito Santo", "GO": "Goiás", "MA": "Maranhão", "MG": "Minas Gerais",
        "MS": "Mato Grosso do Sul", "MT": "Mato Grosso", "PA": "Pará", "PB": "Paraíba", "PE": "Pernambuco",
        "PI": "Piauí", "PR": "Paraná", "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte", "RO": "Rondônia",
        "RR": "Roraima", "RS": "Rio Grande do Sul", "SC": "Santa Catarina", "SE": "Sergipe", "SP": "São Paulo",
        "TO": "Tocantins"
    }
    # Verificar se o estado extraído é válido
    if estado not in estados:
        estado = "Estado não identificado"

    return {
        "data": f"{dia:02}/{mes:02}" if dia and mes else "Data não identificada",
        "hora": hora if hora else "Horário não identificado",
        "evento": titulo_evento,
        "cidade": cidade,
        "estado": estados.get(estado, "Estado não identificado"),
        "link": link
    }

def buscar_eventos(local):
    query = f"eventos em {local}"
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

    options = Options()
    #options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--no-sandbox")

    browser = webdriver.Chrome(options=options)
    browser.get(url)
    #tempo para fazer captcha
    WebDriverWait(browser, 30).until(ExpC.element_to_be_clickable((By.CLASS_NAME,'PBBEhf')))
    more_entries_btn = browser.find_element(By.CLASS_NAME,'PBBEhf')
    more_entries_btn.click()
    WebDriverWait(browser,15).until(ExpC.presence_of_element_located((By.CLASS_NAME, 'SBFvB')))
    eventos = []
    try:
        header_ul = browser.find_element(By.CLASS_NAME, 'SBFvB')
        header_itens = header_ul.find_elements(By.TAG_NAME, 'li')
        bottom_ul = browser.find_element(By.CLASS_NAME, "tl-async-corelist")
        bottom_itens = bottom_ul.find_elements(By.TAG_NAME, 'li')

        for item in header_itens:
            try:
                titulo = item.text
                link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
                eventos.append({'titulo': titulo, 'link': link})
            except Exception as e:
                print(f"[Parser] falhou no item: {e}")
                continue
        for item in bottom_itens:
            try:
                titulo = item.text
                link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
                eventos.append({'titulo': titulo, 'link': link})
            except Exception as e:
                print(f"[Parser] falhou no item: {e}")
                continue

    except Exception as e:
        print("Erro ao capturar box de eventos:", e)
    finally:
        browser.quit()
    print('Formatando resultados...')
    eventos_formatados =[extrair_dados(e) for e in eventos]
    return eventos_formatados
