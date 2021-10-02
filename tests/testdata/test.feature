Feature: Test feature

    This feature is used for basic functional tests of gherlint

    Scenario: Test scenario

        Given the precondition is met
        When I do something
        Then the expected response should happen
         And also something else

    Scenario Outline: Test scenario outline

        Given some precondition
        When I do <x>
        Then I expect <y>

        Examples:
            | x | y |
            | 1 | 2 |
