@any_feature_tag
Feature: Functional test for feature-tags-pattern-missmatch

    Scenario: Feature tags pattern missmatch
        Given I have configured a pattern for future tags
        When I run gherlint
        Then I want feature-tags-pattern-missmatch to trigger

    Scenario: Sample scenario
        Given something
        When something else
        Then something else
