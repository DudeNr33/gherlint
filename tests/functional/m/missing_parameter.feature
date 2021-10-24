Feature: Functional test for missing parameters

    Scenario Outline: Correct outline <name>
        Given the light switch is <on_off>
        When I open my eyes
        Then I will see <visual>

        Examples:
            | name  | on_off | visual  |
            | test1 | off    | nothing |
            | test1 | on     | light   |

    Scenario Outline: Incorrect and missing <y>
        Given the light switch is <state>
        When I open my eyes
        Then I will see <whatever>

        Examples:
            | name  | on_off | visual  |
            | test1 | off    | nothing |
            | test1 | on     | light   |
