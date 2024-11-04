import json
import logging

# Set up logger for config loading
logger = logging.getLogger(__name__)

# Global configuration sets as dictionaries
haram_ingredients = set()
haram_e_numbers = set()
animal_ingredients = set()
cross_contamination_warnings = set()
processing_aids = set()
unreliable_manufacturers = set()
haram_keywords = set()
haram_nutriments = set()

def load_configuration(file_path='./config/halal_config.json'):
    """
    Load the configuration from the JSON file and populate the global sets.
    Each set will now contain dictionaries with 'ingredient', 'code', and 'reason'.
    """
    global haram_ingredients, haram_e_numbers, animal_ingredients
    global cross_contamination_warnings, processing_aids, unreliable_manufacturers
    global haram_keywords, haram_nutriments

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            
            # Load haram ingredients, E-numbers, and others as dictionaries containing code, name, and reason
            haram_ingredients.update(tuple((item['code'], item['ingredient'], item['reason'])) for item in data.get("haram_ingredients", []))
            haram_e_numbers.update(tuple((item['code'], item['e_number'], item['reason'])) for item in data.get("haram_e_numbers", []))
            animal_ingredients.update(tuple((item['code'], item['ingredient'], item['reason'])) for item in data.get("animal_ingredients", []))
            cross_contamination_warnings.update(tuple((item['code'], item['contamination'], item['reason'])) for item in data.get("cross_contamination_warnings", []))
            processing_aids.update(tuple((item['code'], item['aid'], item['reason'])) for item in data.get("processing_aids", []))
            unreliable_manufacturers.update(tuple((item['code'], item['manufacturer'], item['reason'])) for item in data.get("unreliable_manufacturers", []))

            # Load haram keywords and nutriments as sets
            haram_keywords.update(data.get("haram_keywords", []))
            haram_nutriments.update(data.get("haram_nutriments", []))

        logger.info("Configuration loaded successfully from %s", file_path)
    except FileNotFoundError:
        logger.error("No configuration file found at %s", file_path)
        raise FileNotFoundError(f"No configuration file found at {file_path}")
    except json.JSONDecodeError:
        logger.error("Error decoding JSON configuration file at %s", file_path)
        raise ValueError(f"Error decoding JSON configuration file at {file_path}")