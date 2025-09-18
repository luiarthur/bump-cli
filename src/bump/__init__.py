from enum import Enum
from importlib.metadata import version
from pathlib import Path
from typing import Literal

import semver
from git import Repo
from rich.prompt import Confirm
from typer import Option, Typer

__version__ = version("bump-cli")


app = Typer()


class Kind(str, Enum):
    major = "major"
    minor = "minor"
    patch = "patch"
    prerelease = "prerelease"
    build = "build"


@app.command()
def default(
    kind: Kind,
    repo: Path = Option(Path("."), "-r", "--repo", help="Path to git repo."),
    push: bool = Option(
        False,
        "-p",
        "--push",
        help="If present, perform `git push tags` after updating tag.",
    ),
) -> None:
    repo = Repo(repo)
    git_tags = [t.name[1:] for t in repo.tags]
    sorted_git_tags = sorted(git_tags, key=semver.VersionInfo.parse)
    current_tag = sorted_git_tags[-1]

    bump = dict(
        major=semver.bump_major,
        minor=semver.bump_minor,
        patch=semver.bump_patch,
        prerelease=semver.bump_prerelease,
        build=semver.bump_build,
    ).get(kind)

    new_tag = f"v{bump(current_tag)}"

    if Confirm.ask(f"Updating from v{current_tag} to {new_tag}. Proceed?"):
        repo.create_tag(new_tag)
        print(f"Created tag {new_tag}")
        if push:
            repo.remotes.origin.push(new_tag)
            print(f"Pushed tag {new_tag}")
    else:
        print("No updates to git tags.")


def main():
    app()
