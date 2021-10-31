Feature: Functional tests for outline-could-be-a-scenario message

    Scenario Outline: Test without any examples
        Given I accidentally wrote "Scenario Outline" instead of "Scenario"
        When I run gherlint
        Then I want the outline-could-be-a-scenario message to inform me about my mistake

    Scenario Outline: Test with just one example
        Given I actually included examples
        But I only have a single set of examples (<example>)
        When I run gherlint
        Then I want it to inform me that this could be a normal scenario

        Examples:
            | example |
            | foo     |

    Scenario Outline: Test with multiple examples across more than one Examples keyword
        Given I included more than just one example (<example>)
        When I run gherlint
        Then I don't want it to trigger the message

        Examples: First set
            | example |
            | Value 1 |

        Examples: Second set
            | example |
            | Value 2 |

    Scenario Outline: Test with multiple examples
        Given I included more than just one example (<example>)
        When I run gherlint
        Then I don't want it to trigger the message

        Examples:
            | example |
            | Value 1 |
            | Value 2 |
