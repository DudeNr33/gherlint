"""
``gherlint`` is a linter for Cucumber Gherkin feature files.
"""
import click

from gherlint.linter import GherkinLinter


@click.command()
@click.argument("path")
def main(path):
    GherkinLinter(path).run()


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
