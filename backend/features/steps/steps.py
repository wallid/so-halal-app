# features/steps/steps.py

from behave import given, when, then
from src.services.halal_strategies import (
    IngredientBasedStrategy,
    ENumberBasedStrategy,
    KeywordBasedStrategy,
    NutritionBasedStrategy,
)
from src.services.halal_verification import verify_halal
from src.models.enums import HalalStatus
from src.util.config import (
    haram_ingredients,
    haram_e_numbers,
    haram_keywords,
    haram_nutriments,
)

# Given Steps
# features/steps/steps.py

@given('a product with ingredients "{ingredients}"')
def step_given_product_with_ingredients(context, ingredients):
    if not hasattr(context, "product_info"):
        context.product_info = {}
    context.product_info["ingredients_tags"] = [f'en:{ingredient.strip()}' for ingredient in ingredients.split(',')]

@given('a product with additives "{additives}"')
def step_given_product_with_additives(context, additives):
    if not hasattr(context, "product_info"):
        context.product_info = {}
    context.product_info["additives_tags"] = [f'en:{additive.strip().lower()}' for additive in additives.split(',')]

@given('a product with keywords "{keywords}"')
def step_given_product_with_keywords(context, keywords):
    if not hasattr(context, "product_info"):
        context.product_info = {}
    context.product_info["_keywords"] = [keyword.strip().lower() for keyword in keywords.split(',')]

@given('a product with nutriments "{nutriments}"')
def step_given_product_with_nutriments(context, nutriments):
    if not hasattr(context, "product_info"):
        context.product_info = {}
    nutriments_dict = {}
    for nutriment in nutriments.split(','):
        key, value = nutriment.strip().split(':')
        nutriments_dict[key.strip().lower()] = float(value.strip())
    context.product_info["nutriments"] = nutriments_dict


# When Steps
@when('I check if the product is halal using the ingredient-based strategy')
def step_when_check_ingredient_based(context):
    strategy = IngredientBasedStrategy()
    context.status, context.haram_found, context.reasons = strategy.is_halal(context.product_info)

@when('I check if the product is halal using the E-number based strategy')
def step_when_check_enumber_based(context):
    strategy = ENumberBasedStrategy()
    context.status, context.haram_found, context.reasons = strategy.is_halal(context.product_info)

@when('I check if the product is halal using the keyword-based strategy')
def step_when_check_keyword_based(context):
    strategy = KeywordBasedStrategy()
    context.status, context.haram_found, context.reasons = strategy.is_halal(context.product_info)

@when('I check if the product is halal using the nutrition-based strategy')
def step_when_check_nutrition_based(context):
    strategy = NutritionBasedStrategy()
    context.status, context.haram_found, context.reasons = strategy.is_halal(context.product_info)

@when('I verify if the product is halal')
def step_when_verify_halal(context):
    context.result = verify_halal(context.product_info)

# Then Steps
@then('the result should be "{expected_result}"')
def step_then_verify_result(context, expected_result):
    status_mapping = {
        "Not Halal": HalalStatus.NOT_HALAL,
        "Halal": HalalStatus.HALAL,
        "Halal Given Ingredients": HalalStatus.HALAL_GIVEN_INGREDIENTS,
        "Not Enough Information": HalalStatus.NOT_ENOUGH_INFORMATION,
    }
    expected = status_mapping.get(expected_result)
    # For the strategies, context.status is a HalalStatus enum
    assert context.status == expected, f"Expected {expected}, got {context.status}"

@then('haram ingredients found should be "{ingredients}"')
def step_then_haram_ingredients(context, ingredients):
    expected_set = {ingredient.strip().lower() for ingredient in ingredients.split(',')}
    actual_set = {item.lower() for item in context.haram_found}
    assert actual_set == expected_set, f"Expected {expected_set}, got {actual_set}"

# Continue similarly for other 'then' steps

# For the 'overall' verification
@then('the overall status should be "{expected_status}"')
def step_then_overall_status(context, expected_status):
    status_mapping = {
        "Not Halal": HalalStatus.NOT_HALAL,
        "Halal": HalalStatus.HALAL,
        "Halal Given Ingredients": HalalStatus.HALAL_GIVEN_INGREDIENTS,
        "Not Enough Information": HalalStatus.NOT_ENOUGH_INFORMATION,
    }
    expected = status_mapping.get(expected_status)
    actual = context.result["status"]
    assert actual == expected, f"Expected status {expected}, but got {actual}"

@then('haram items found should be "{items}"')
def step_then_haram_items(context, items):
    expected_set = {item.strip().lower() for item in items.split(',')}
    actual_set = {item.lower() for item in context.result["haram_items_found"]}
    assert actual_set == expected_set, f"Expected haram items {expected_set}, but got {actual_set}"


@then('haram E-numbers found should be "{enumbers}"')
def step_then_haram_enumbers(context, enumbers):
    expected_set = {enumber.strip().lower() for enumber in enumbers.strip('"').split(',')}
    actual_set = {item.lower() for item in context.haram_found}
    assert actual_set == expected_set, f"Expected {expected_set}, got {actual_set}"


@then(u'no haram E-numbers should be found')
def step_then_no_haram_enumbers(context):
    assert not context.haram_found, f"Expected no haram E-numbers, but found {context.haram_found}"


@then(u'no haram ingredients should be found')
def step_impl(context):
    assert not context.haram_found, f"Expected no haram ingredients, but found {context.haram_found}"

@then(u'no haram keywords should be found')
def step_impl(context):
    assert not context.haram_found, f"Expected no haram keywords, but found {context.haram_found}"

@then(u'haram keywords found should be "{keywords}"')
def step_then_haram_keywords(context, keywords):
    # Parse the expected keywords from the Gherkin step
    expected_keywords = {keyword.strip().lower() for keyword in keywords.split(',')}
    
    # Assert that the found haram keywords in context match the expected keywords
    assert context.haram_found == expected_keywords, f"Expected haram keywords {expected_keywords}, but found {context.haram_found}"


@then(u'no haram nutriments should be found')
def step_then_no_haram_nutriments(context):
    # Assert that haram_found is empty, indicating no haram nutriments were found
    assert not context.haram_found, f"Expected no haram nutriments, but found {context.haram_found}"


@then(u'haram nutriments found should be "{nutriments}"')
def step_impl(context, nutriments):
    # Parse the expected nutriments from the Gherkin step
    expected_nutriments = {nutriment.strip().lower() for nutriment in nutriments.split(',')}
    
    # Assert that the found haram nutriments in context match the expected nutriments
    assert context.haram_found == expected_nutriments, f"Expected haram nutriments {expected_nutriments}, but found {context.haram_found}"


@then(u'no haram items should be found')
def step_impl(context):
    # Assert that haram_items_found is empty, indicating no haram items were found
    assert not context.result["haram_items_found"], f"Expected no haram items, but found {context.result['haram_items_found']}"