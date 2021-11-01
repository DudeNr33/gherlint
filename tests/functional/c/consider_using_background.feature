Feature: Functional test for consider-using-background

    Scenario: My first scenario
        Given a common precondition
        And a second common precondition
        And a precondition used multiple times but not always
        And a custom precondition
        When I run gherlint
        Then it should trigger the consider-using-background message for the first two

    Scenario Outline: My second scenario is an outline
        Given a common precondition
        And a second common precondition
        And a precondition used multiple times but not always
        And some other custom precondition with parameter <foo>
        When I run gherlint
        Then it should trigger the consider-using-background message for the first two

        Examples:
            | foo |
            | a   |
            | b   |

    Scenario: My third scenario
        Given a common precondition
        And a second common precondition
        When I run gherlint
        Then it should trigger the consider-using-background message for the first two
