Feature: Functional test for only-given-allowed-in-background

    Background: Bad background
        Given I have a given step, which is OK
        And I have another given step, which is also OK
        When I add a when step
        And another one
        Then also a then step

    Scenario: Sample scenario
        Given something
        When something else
        Then something else

    Scenario: Another scenario
        Given something else
        When something else
        Then something else
