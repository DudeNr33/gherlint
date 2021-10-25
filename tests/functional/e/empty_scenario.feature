Feature: Functional test for empty-scenario

    Scenario: OK scenario
        Given a precondition
        When I do x
        Then I expect y

    Scenario: Empty scenario

    Scenario Outline: Empty scenario outline

    Scenario: Empty but with description

        This scenario has a description, but still the empty-scenario message should
        trigger because there are no steps!
