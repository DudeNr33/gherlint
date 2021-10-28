Feature: Functional test for unused-parameter

    Scenario Outline: My Outline
        Given I have a parameter <x>
        When I also have parameter <y> but not z
        Then I expect unused-parameter to trigger

        Examples:
            | x   | y   | z   |
            | 1   | 2   | 3   |
            | foo | bar | baz |
