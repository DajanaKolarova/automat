import requests
import logging

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
            try:
                response = requests.get(url)
                response.raise_for_status()
                page_html = response.text

                # Dynamically set the field on the model
                field_name = f"jidelnicek_{jidelna}"
                if hasattr(denni_menu, field_name):
                    setattr(denni_menu, field_name, page_html)
                    logger.info(f"Successfully updated {field_name}.")
                else:
                    logger.warning(f"Field {field_name} does not exist in the model.")
            except requests.RequestException as e:
                logger.error(f"Failed to scrape {jidelna}: {e}")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")

