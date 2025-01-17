from argparse import ArgumentParser

import semver
from git import Repo


def parse_args():
    parser = ArgumentParser("bumpy")
    parser.add_argument(
        "kind",
        choices=["major", "minor", "patch", "prerelease", "build"],
    )
    parser.add_argument("-r", "--repo", default=".", help="Path to git repo.")
    parser.add_argument(
        "-p",
        "--push",
        action="store_true",
        help="If present, perform `git push --tags` after updating tag.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    repo = Repo(args.repo)
    git_tags = [t.name[1:] for t in repo.tags]
    sorted_git_tags = sorted(git_tags, key=semver.VersionInfo.parse)
    current_tag = sorted_git_tags[-1]

    bump = dict(
        major=semver.bump_major,
        minor=semver.bump_minor,
        patch=semver.bump_patch,
        prerelease=semver.bump_prerelease,
        build=semver.bump_build,
    ).get(args.kind)

    new_tag = f"v{bump(current_tag)}"

    response = (
        input(f"Updating from v{current_tag} to {new_tag}. Proceed? [yes/no]: ")
        .strip()
        .lower()
    )

    if response == "yes":
        repo.create_tag(new_tag)
        print(f"Created tag {new_tag}")
        if args.push:
            repo.remotes.origin.push(new_tag)
            print(f"Pushed tag {new_tag}")
    else:
        print("No updates to git tags.")
