# features/nutrition_based_strategy.feature

Feature: Nutrition-Based Halal Verification
  As a user
  I want to verify if a product is halal based on its nutriments
  So that I can avoid products with haram nutriments

  Scenario: Product contains haram nutriments
    Given a product with nutriments "alcohol: 5"
    When I check if the product is halal using the nutrition-based strategy
    Then the result should be "Not Halal"
    And haram nutriments found should be "alcohol"

  Scenario: Product does not contain haram nutriments
    Given a product with nutriments "sugar: 10"
    When I check if the product is halal using the nutrition-based strategy
    Then the result should be "Halal"
    And no haram nutriments should be found
