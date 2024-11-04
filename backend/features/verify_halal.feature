# features/verify_halal.feature

Feature: Overall Halal Verification
  As a user
  I want to verify if a product is halal using all strategies
  So that I can get an overall halal status

  # Background:
  #   Given the halal configuration is loaded

  Scenario: Product is not halal due to haram ingredients
    Given a product with ingredients "gelatin"
    And a product with additives "E100"
    And a product with keywords "snack"
    And a product with nutriments "sugar:10"
    When I verify if the product is halal
    Then the overall status should be "Not Halal"
    And haram items found should be "gelatin"

  Scenario: Product is not halal due to haram E-numbers
    Given a product with ingredients "sugar"
    And a product with additives "E441"
    And a product with keywords "candy"
    And a product with nutriments "sugar:10"
    When I verify if the product is halal
    Then the overall status should be "Not Halal"
    And haram items found should be "E441"

  Scenario: Product is not halal due to haram keywords
    Given a product with ingredients "water"
    And a product with additives "E100"
    And a product with keywords "alcoholic"
    And a product with nutriments "sugar:5"
    When I verify if the product is halal
    Then the overall status should be "Not Halal"
    And haram items found should be "alcoholic"

  Scenario: Product is not halal due to haram nutriments
    Given a product with ingredients "water"
    And a product with additives "E100"
    And a product with keywords "drink"
    And a product with nutriments "alcohol:5"
    When I verify if the product is halal
    Then the overall status should be "Not Halal"
    And haram items found should be "alcohol"

  Scenario: Product is halal
    Given a product with ingredients "water"
    And a product with additives "E100"
    And a product with keywords "drink"
    And a product with nutriments "sugar:5"
    When I verify if the product is halal
    Then the overall status should be "Halal"
    And no haram items should be found
