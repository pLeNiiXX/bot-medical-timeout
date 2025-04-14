
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import time
import os

# Telegram config (usa tus tokens aquí)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Palabras clave para detectar eventos importantes
keywords = ["medical", "injury", "trainer", "timeout", "treatment"]

# Configuración de Chrome en modo headless para Render
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def enviar_telegram(texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": texto})

def scrapear_sofascore():
    driver.get("https://www.sofascore.com/es/tenis")
    time.sleep(5)

    partidos = driver.find_elements(By.CSS_SELECTOR, "a[href*='/partido/']")
    enlaces_partidos = list({p.get_attribute('href') for p in partidos if p.get_attribute('href')})

    for enlace in enlaces_partidos:
        driver.get(enlace)
        time.sleep(3)
        comentarios = driver.page_source.lower()

        for palabra in keywords:
            if palabra in comentarios:
                enviar_telegram(f"🚨 ¡Posible lesión! Detectado '{palabra.upper()}' en:\n{enlace}")
                print(f"[ALERTA] Encontrado '{palabra}' en {enlace}")
                break

try:
    while True:
        scrapear_sofascore()
        print("Esperando 120 segundos...\n")
        time.sleep(120)
except KeyboardInterrupt:
    print("Bot detenido.")
finally:
    driver.quit()
