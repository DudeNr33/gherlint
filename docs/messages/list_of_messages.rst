List of Messages
================

.. list-table::
   :header-rows: 1

   * - ID
     - Name
     - Description
   * - E001
     - unparseable-file
     - File could not be parsed: {error_msg}
   * - E002
     - missing-language-tag
     - A feature file which uses an other language than English should declare this with a '# language: <lang>' tag at the beginning of the file.
   * - E003
     - wrong-language-tag
     - Language tag does not match the language used
   * - W101
     - missing-feature-name
     - Feature has no name
   * - W102
     - missing-scenario-name
     - Scenario has no name
   * - E101
     - missing-parameter
     - '{parameter}' is not defined in the Examples section
   * - W103
     - file-has-no-feature
     - No Feature given in file
   * - W104
     - empty-feature
     - Feature has no scenarios
   * - W105
     - empty-scenario
     - Scenario does not contain any steps
   * - W106
     - empty-background
     - Background does not contain any steps
   * - C101
     - missing-given-step
     - Scenario does not contain any Given step
   * - C102
     - missing-when-step
     - Scenario does not contain any When step
   * - C103
     - missing-then-step
     - Scenario does not contain any Then step
   * - R101
     - unused-parameter
     - Parameter '{parameter}' is not used
   * - R201
     - outline-could-be-a-scenario
     - This outline contains no or only one example, consider using a normal scenario instead
   * - R202
     - consider-using-background
     - Consider putting common 'Given' steps in a Background
   * - E301
     - examples-outside-scenario-outline
     - Examples used outside a Scenario Outline
   * - W301
     - duplicated-tag
     - Tag '{tag}' already present on the parent element
   * - C301
     - duplicated-scenario-name
     - Scenarios inside a Feature should have unique names
