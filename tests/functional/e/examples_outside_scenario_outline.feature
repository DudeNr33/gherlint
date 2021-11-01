Feature: Functional test for examples-outside-scenario-outline

    Scenario: My Test
        Given some precondition
        When I forget to write "Scenario Outline"
        And I add examples like <foo>
        Then I want examples-outside-scenario-outline to trigger

        Examples: My parameters
            | foo  |
            | test |
            | bar  |

    Scenario: Another test
        Given I have examples
        When I don't actually use any of the parameters
        Then I still want examples-outside-scenario-outline to trigger

        Examples: First Set
            | foo  |
            | test |
            | bar  |

        Examples: Second Set
            | foo  |
            | spam |
            | eggs |
