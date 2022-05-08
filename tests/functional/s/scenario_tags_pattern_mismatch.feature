Feature: Functional test for scenario-tags-pattern-mismatch

    @any_scenario_tag @success
    Scenario: Scenario tags pattern missmatch
        Given I have configured a pattern for scenario tags
        When I run gherlint
        Then I want scenario-tags-pattern-missmatch to trigger

    @any_scenario_tag @fail
    Scenario Outline: Scenario Outline tags pattern missmatch
        Given I have configured a pattern for scenario tags
        When I run gherlint with <test>
        Then I want scenario-tags-pattern-missmatch to trigger

        Examples:
            | test |
            | 1    |
            | 2    |

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
