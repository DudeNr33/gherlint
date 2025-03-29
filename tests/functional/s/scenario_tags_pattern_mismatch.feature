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

    @success
    Scenario: Only success tag
        Given something
        When something else
        Then something else

    @fail
    Scenario: Only fail tag
        Given something
        When something else
        Then something else

    @wip
    Scenario: Only wip tag
        Given something
        When something else
        Then something else

    @wip @jira-001
    Scenario: wip tag and jira tag
        Given something
        When something else
        Then something else

    @wip @jira-002 @slow
    Scenario: All tags
        Given something
        When something else
        Then something else

    @success @slow
    Scenario: success tag and slow tag
        Given something
        When something else
        Then something else

    @jira-003 @success
    Scenario: Wrong order, but it's ok
        Given something
        When something else
        Then something else

    @jira-004
    @success
    Scenario: Multiline tags
        Given something
        When something else
        Then something else
