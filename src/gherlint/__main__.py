"""
``gherlint`` is a linter for Cucumber Gherkin feature files.
"""
from pathlib import Path

import click

from gherlint.linter import GherkinLinter
from gherlint.statistics import compute_metrics


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """gherlint is a linter for Cucumber Gherkin feature files."""
    if ctx.invoked_subcommand is None:
        print(cli.get_help(ctx))


@cli.command()
@click.argument("path")
def lint(path: str) -> None:
    """Perform linting of feature files"""
    GherkinLinter(Path(path)).run()


@cli.command()
@click.argument("path")
def stats(path: str) -> None:
    """Compute metrics over your feature files"""
    compute_metrics(Path(path))


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
