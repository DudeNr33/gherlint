Feature: Functional test for tag-could-be-on-feature

    @mytag
    Scenario: First scenario
        Given I have a feature with a tag
        When I run gherlint
        Then I want tag-could-be-on-feature to trigger

    @mytag
    Scenario: Second scenario
        Given I have another feature with the same tag
        When I run gherlint
        Then I want tag-could-be-on-feature to trigger

    @mytag
    @someothertag
    Scenario: Third scenario
        Given I have a feature with the same tag and another tag
        When I run gherlint
        Then I want tag-could-be-on-feature to trigger only for the tag that appears on all features

    @mytag
    Scenario Outline: My scenario outline
        Given I have multiple examples with the same tag <tag>
        When I run gherlint
        Then I want tag-could-be-on-feature to trigger

        @commontag
        @customtag
        Examples: first set
            | tag |
            | foo |
            | bar |

        @othercustomtag
        @commontag
        Examples: second set
            | tag  |
            | spam |
            | eggs |
