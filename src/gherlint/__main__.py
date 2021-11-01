"""
``gherlint`` is a linter for Cucumber Gherkin feature files.
"""
from pathlib import Path

import click

from gherlint.fixer import LanguageFixer
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


@cli.command()
@click.option(
    "--dry-run",
    default=False,
    is_flag=True,
    help="Don't write to disk, only output which files would be modified",
)
@click.argument("path")
def fix_language_tags(path: str, dry_run: bool) -> None:
    """Add or fix language tags in feature files

    If gherlint detects that a language other than English is used, it will
    try to infer the correct language and add the corresponding tag.
    If a language tag is present but does not fit to the file contents, the existing
    tag will be replaced.
    """
    LanguageFixer(Path(path)).run(modify=not dry_run)


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
