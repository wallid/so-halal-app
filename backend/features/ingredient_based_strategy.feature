# features/ingredient_based_strategy.feature

Feature: Ingredient-Based Halal Verification
  As a user
  I want to verify if a product is halal based on its ingredients
  So that I can avoid products with haram ingredients

  Scenario: Product contains haram ingredients
    Given a product with ingredients "bacon, water, salt"
    When I check if the product is halal using the ingredient-based strategy
    Then the result should be "Not Halal"
    And haram ingredients found should be "bacon"

  Scenario: Product contains new haram ingredients
    Given a product with ingredients "gelatin, sugar, water"
    When I check if the product is halal using the ingredient-based strategy
    Then the result should be "Not Halal"
    And haram ingredients found should be "gelatin"

  Scenario: Product does not contain haram ingredients
    Given a product with ingredients "water, sugar, salt"
    When I check if the product is halal using the ingredient-based strategy
    Then the result should be "Halal"
    And no haram ingredients should be found
