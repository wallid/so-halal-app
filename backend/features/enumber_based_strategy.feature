# features/enumber_based_strategy.feature

Feature: E-Number Based Halal Verification
  As a user
  I want to verify if a product is halal based on its E-numbers
  So that I can avoid products with haram E-numbers

  Scenario: Product contains haram E-numbers
    Given a product with additives "E120"
    When I check if the product is halal using the E-number based strategy
    Then the result should be "Not Halal"
    And haram E-numbers found should be "E120"

  Scenario: Product does not contain haram E-numbers
    Given a product with additives "E100, E101"
    When I check if the product is halal using the E-number based strategy
    Then the result should be "Halal"
    And no haram E-numbers should be found
