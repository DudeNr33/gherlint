Feature: Test

    Scenario:
        Given some precondition
        When I do something
        Then I expect some outcome

    Scenario Outline:
        Given some precondition <pre>
        When I do something
        Then I expect some outcome

        Examples:
            | pre |
            | foo |
            | bar |
