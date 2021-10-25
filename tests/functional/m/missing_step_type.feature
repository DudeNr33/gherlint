Feature: Functional tests for missing-<xy>-step

    This feature tests all possible variations of the missing-<xy>-step messages

    Scenario: Missing Given
        When I leave out the Given step
        Then I expect missing-given-step to trigger

    Scenario: Missing When step
        Given I leave out the When step
        Then I expect missing-when-step to trigger

    Scenario: Missing Then step
        Given I leave out the Then step
        When gherlint runs

    Scenario: Missing multiple step types
        Then I expect both missing-given-step and missing-then-step to trigger
