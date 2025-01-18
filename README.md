# Bump

A command line tool for bumping git tag versions.

## Install

**pip**
```
pip install bump-cli
```

**uv**
```
uv tool install bump-cli
```


## Usage


```
usage: bump [-h] [-r REPO] [-p] {major,minor,patch,prerelease,build}

positional arguments:
  {major,minor,patch,prerelease,build}

optional arguments:
  -h, --help            show this help message and exit
  -r REPO, --repo REPO  Path to git repo.
  -p, --push            If present, perform `git push --tags` after updating tag.
```

