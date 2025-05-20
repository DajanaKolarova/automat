import requests
import logging
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract


# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def scrape_and_save_denni_menu():
    urls = {
    
        "technicka_menza": "https://agata.suz.cvut.cz/jidelnicky/indexTyden.php?clPodsystem=3&lang=cs",
        "restaurant_kulatak": "https://kulatak.cz/#menu-obsah", # pomocí beautiful soup najít si v web inspector paragrafy <p jednotlivých jídel který vyprintuješ
        "restaurant_utopolu": "https://www.utopolu.cz/menu", #je to obrázek takže musím použít OCR pytesseract 
        #cafe organica potřebuju login přes selenium nebo cookies
    }

    try:
        # Create or update a single entry for the daily menu
       
        for jidelna, url in urls.items():       
            response = requests.get(url)
            response.raise_for_status()
            page_html = response.text
            
            
            soup = BeautifulSoup(page_html)
            print(soup)

            print(soup.prettify())


    except Exception as e:
        logger.error(f"Unexpected error: {e}")

