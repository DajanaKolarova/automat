import requests
import logging
from .models import JidelnaCVUT, JidelnaCVUTDenniMenu # asdf
from celery import shared_task

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@shared_task
def scrape_and_save_denni_menu():
    urls = {
        "menza_studentskyDum": "https://agata.suz.cvut.cz/jidelnicky/index.php?clPodsystem=2&lang=cs",
        "technicka_menza": "https://agata.suz.cvut.cz/jidelnicky/index.php?clPodsystem=3&lang=cs",
    }

    try:
        # Create or update a single entry for the daily menu
        denni_menu, created = JidelnaCVUTDenniMenu.objects.get_or_create()

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

        # Save all changes to the database
        denni_menu.save()
        logger.info("Successfully saved the daily menu.")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")


@shared_task
def scrape_jidelna_cvut():
    url = "https://agata.suz.cvut.cz/jidelnicky/indexTyden.php?clPodsystem=1&lang=cs"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the request failed
        page_html = response.text

        # Save the HTML to the JidelnaCVUT model
        JidelnaCVUT.objects.create(page_html=page_html)
        logger.info("Successfully scraped and saved Jidelna CVUT page.")
    except requests.RequestException as e:
        # Log the error or handle it as needed
        logger.error(f"Failed to scrape JidelnaCVUT: {e}")
