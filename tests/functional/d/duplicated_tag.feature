@alreadyonfeature
@myuniquetag
Feature: Functional test for duplicated-tag

    @alreadyonfeature
    @myotheruniquetag
    Scenario: My first scenario
        Given I have a tag that appears on both the Feature and the Scenario
        When I run gherlint
        Then I want the duplicated-tag message to fire for the Scenario

    @alreadyonfeature
    @alreadyonoutline
    Scenario Outline: My second scenario
        Given I have a tag that appears on both the Feature and the Scenario Outline
        And I use a parameter <foo>
        When I run gherlint
        Then I want the duplicated-tag message to fire for the Scenario

        @alreadyonfeature
        @alreadyonoutline
        @exampleunique
        Examples:
            | foo |
            | bar |
            | baz |
