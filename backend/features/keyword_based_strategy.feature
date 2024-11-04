# features/keyword_based_strategy.feature

Feature: Keyword-Based Halal Verification
  As a user
  I want to verify if a product is halal based on its keywords
  So that I can avoid products with haram-related keywords

  Scenario: Product contains haram keywords
    Given a product with keywords "wine, beverage"
    When I check if the product is halal using the keyword-based strategy
    Then the result should be "Not Halal"
    And haram keywords found should be "wine"

  Scenario: Product contains new haram keywords
    Given a product with keywords "alcoholic, drink"
    When I check if the product is halal using the keyword-based strategy
    Then the result should be "Not Halal"
    And haram keywords found should be "alcoholic"

  Scenario: Product does not contain haram keywords
    Given a product with keywords "juice, beverage"
    When I check if the product is halal using the keyword-based strategy
    Then the result should be "Halal"
    And no haram keywords should be found
