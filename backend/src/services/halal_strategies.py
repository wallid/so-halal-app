# src/services/halal_strategies.py

from abc import ABC, abstractmethod
from typing import Set, Dict, Any
import logging
from src.util.config import haram_ingredients, haram_e_numbers, haram_keywords, haram_nutriments
from src.models.enums import HalalStatus

# Configure logging
logging.basicConfig(
    filename='./logs/halal_verification.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

# Abstract base class for halal verification strategies
class HalalVerificationStrategy(ABC):
    @abstractmethod
    def is_halal(self, product_info: Dict[str, Any]) -> (HalalStatus, Set[str], Set[str]):
        pass

# Registry for strategies
strategy_registry = {}

def strategy(name: str):
    def decorator(cls):
        strategy_registry[name] = cls
        return cls
    return decorator

def get_strategy(name: str):
    strategy_cls = strategy_registry.get(name)
    if not strategy_cls:
        raise ValueError(f"Strategy '{name}' not found.")
    return strategy_cls

class StrategyFactory:
    def __init__(self):
        self.strategies = []

    def register_strategy(self, strategy: HalalVerificationStrategy):
        self.strategies.append(strategy)

    def get_strategies(self):
        return self.strategies

# Ingredient-based strategy

@strategy("ingredient_based")
class IngredientBasedStrategy(HalalVerificationStrategy):
    def __init__(self):
        # Use the globally loaded haram ingredients set of tuples
        self.haram_ingredients = haram_ingredients
        logger.info("Initialized IngredientBasedStrategy with haram ingredients: %s", self.haram_ingredients)

    def is_halal(self, product_info: Dict[str, Any]) -> (HalalStatus, Set[str], Set[str]):
        # Extract and normalize product ingredients
        ingredients = product_info.get("ingredients_tags", [])
        ingredients = [tag.split(':')[-1].lower() for tag in ingredients]
        logger.info("Product ingredients: %s", ingredients)

        # Find haram ingredients and collect reasons
        haram_found = set()
        reasons = set()

        for ingredient in ingredients:
            logger.debug("Checking ingredient: %s", ingredient)
            for _, haram_ingredient, reason in self.haram_ingredients:
                if ingredient == haram_ingredient:
                    haram_found.add(ingredient)
                    reasons.add(f"{ingredient}: {reason}")
                    break  # No need to check further once a match is found

        if haram_found:
            logger.info("Haram ingredients found: %s", haram_found)
            return HalalStatus.NOT_HALAL, haram_found, reasons

        logger.info("No haram ingredients found.")
        return HalalStatus.HALAL, set(), set()

# E-number based strategy
@strategy("enumber_based")
class ENumberBasedStrategy(HalalVerificationStrategy):
    def __init__(self):
        # Use the globally loaded haram E-numbers as a set of tuples
        self.haram_e_numbers = haram_e_numbers
        logger.info("Initialized ENumberBasedStrategy with haram E-numbers: %s", self.haram_e_numbers)

    def is_halal(self, product_info: Dict[str, Any]) -> (HalalStatus, Set[str], Set[str]):
        # Extract and normalize product additives
        additives = product_info.get("additives_tags", [])
        additives = [tag.split(':')[-1].lower() for tag in additives]
        logger.debug("Product additives: %s", additives)

        # Identify haram E-numbers and collect reasons
        haram_found = set()
        reasons = set()

        for additive in additives:
            for code, e_number, reason in self.haram_e_numbers:
                if additive == e_number:
                    haram_found.add(e_number)
                    reasons.add(f"{e_number}: {reason}")

        if haram_found:
            logger.info("Haram E-numbers found: %s", haram_found)
            return HalalStatus.NOT_HALAL, haram_found, reasons

        logger.info("No haram E-numbers found.")
        return HalalStatus.HALAL, set(), set()

# Keyword-based strategy
@strategy("keyword_based")
class KeywordBasedStrategy(HalalVerificationStrategy):
    def __init__(self):
        self.haram_keywords = haram_keywords
        logger.info("Initialized KeywordBasedStrategy with haram keywords: %s", self.haram_keywords)

    def is_halal(self, product_info: Dict[str, Any]) -> (HalalStatus, Set[str], Set[str]):
        keywords = product_info.get("_keywords", [])
        keywords = [kw.lower() for kw in keywords]
        logger.debug("Product keywords: %s", keywords)

        haram_found = set(keywords) & self.haram_keywords
        if haram_found:
            reasons = {f"Contains haram keyword: {kw}" for kw in haram_found}
            logger.info("Haram keywords found: %s", haram_found)
            return HalalStatus.NOT_HALAL, haram_found, reasons
        logger.info("No haram keywords found.")
        return HalalStatus.HALAL, set(), set()

# Nutrition-based strategy
@strategy("nutrition_based")
class NutritionBasedStrategy(HalalVerificationStrategy):
    def __init__(self):
        self.haram_nutriments = haram_nutriments
        logger.info("Initialized NutritionBasedStrategy with haram nutriments: %s", self.haram_nutriments)

    def is_halal(self, product_info: Dict[str, Any]) -> (HalalStatus, Set[str], Set[str]):
        nutriments = product_info.get("nutriments", {})
        logger.debug("Product nutriments: %s", nutriments)

        haram_found = {nutriment for nutriment, value in nutriments.items()
                       if nutriment in self.haram_nutriments and value > 0}
        if haram_found:
            reasons = {f"Contains haram nutriment: {nutriment}" for nutriment in haram_found}
            logger.info("Haram nutriments found: %s", haram_found)
            return HalalStatus.NOT_HALAL, haram_found, reasons
        logger.info("No haram nutriments found.")
        return HalalStatus.HALAL, set(), set()

def initialize_strategies():
    factory = StrategyFactory()
    factory.register_strategy(IngredientBasedStrategy())
    factory.register_strategy(ENumberBasedStrategy())
    factory.register_strategy(KeywordBasedStrategy())
    factory.register_strategy(NutritionBasedStrategy())
    return factory
