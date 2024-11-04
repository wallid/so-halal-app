from enum import Enum

class HalalStatus(str, Enum):
    HALAL = "halal"
    NOT_HALAL = "not_halal"
    HALAL_GIVEN_INGREDIENTS = "halal_given_ingredients"
    NOT_ENOUGH_INFORMATION = "not_enough_information"
    UNKNOWN = "unknown"  # For cases where status can't be determined
