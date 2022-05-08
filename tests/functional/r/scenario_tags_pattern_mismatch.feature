Feature: Functional test for missing-required-scenario-tags

    @any_scenario_tag
    Scenario: Missing required scenario tags
        Given I have configured required scenario tags
        When I run gherlint
        Then I want missing-required-scenario-tags to trigger

    @success
    Scenario: Sample scenario
        Given something
        When something else
        Then something else

    @fail
    Scenario: Sample scenario 2
        Given something
        When something else
        Then something else

    @JIRA-999
    Scenario: Sample scenario 3
        Given something
        When something else
        Then something else

    @wip
    Scenario: Sample scenario 4
        Given something
        When something else
        Then something else
