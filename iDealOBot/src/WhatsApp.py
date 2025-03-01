import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from Offer import Offer

class WhatsApp:
    def send(self, offerData:Offer):

        # WebDriver starten
        driver = webdriver.Chrome()  
        driver.get("https://web.whatsapp.com")

        input("Scanne den QR-Code und drücke Enter...")  # Manuelle Anmeldung

        # Zur Gruppe navigieren
        group_name = "iDealOMat"
        search_box = driver.find_element(By.XPATH, '//div[@title="Suchen"]')
        search_box.click()
        search_box.send_keys(group_name)
        search_box.send_keys(Keys.ENTER)

        # Nachricht senden
        message_box = driver.find_element(By.XPATH, '//div[@title="Nachricht schreiben"]')
        message_box.send_keys("Hallo Gruppe, das ist eine Testnachricht!")
        message_box.send_keys(Keys.ENTER)

        time.sleep(2)
        driver.quit()