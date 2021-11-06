Feature: Functional test for duplicated-scenario-name

    Scenario: Unique name
        Given I have a scenario with an unique name
        When I run gherlint
        Then I don't want duplicated-scenario-name to trigger

    Scenario: Reused scenario name
        Given I have a scenario with a name that is used multiple times in a feature
        When I run gherlint
        Then I want duplicated-scenario-name to trigger

    Scenario: Reused scenario name
        Given I have a second scenario with the same name
        When I run gherlint
        Then I want duplicated-scenario-name to trigger

    Scenario Outline: Reused scenario name
        Given I have a scenario outline with the same name as a scenario and a parameter <test>
        When I run gherlint
        Then I want duplicated-scenario-name to trigger for the outline as well

        Examples:
            | test |
            | foo  |
            | foo  |
