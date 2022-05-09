Feature: Functional test for scenario-tags-pattern-mismatch

    @any_scenario_tag @success
    Scenario: Scenario tags pattern missmatch due to unknown tag
        Given I have configured a pattern for scenario tags
        When I run gherlint
        Then I want scenario-tags-pattern-missmatch to trigger

    @any_scenario_tag @fail
    Scenario Outline: Scenario Outline tags pattern missmatch due to unknown tag
        Given I have configured a pattern for scenario tags
        When I run gherlint with <test>
        Then I want scenario-tags-pattern-missmatch to trigger

        Examples:
            | test |
            | 1    |
            | 2    |

    @jira-001 @success
    Scenario: Scenario tags pattern missmatch due to wrong order
        Given I have configured a pattern for scenario tags
        When I run gherlint
        Then I want scenario-tags-pattern-missmatch to trigger

    @success
    Scenario: Only required success tag
        Given something
        When something else
        Then something else

    @fail
    Scenario: Only required fail tag
        Given something
        When something else
        Then something else

    @wip
    Scenario: Only required wip tag
        Given something
        When something else
        Then something else

    @wip @jira-002
    Scenario: Required wip tag and optional jira tag
        Given something
        When something else
        Then something else

    @wip @jira-003 @slow
    Scenario: All tags
        Given something
        When something else
        Then something else

    @success @slow
    Scenario: Required success tag and optional slow tag
        Given something
        When something else
        Then something else
