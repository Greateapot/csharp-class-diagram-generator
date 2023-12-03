import argparse
import os

from cscdg.models.project import Project


def main():
    parser = argparse.ArgumentParser(description="Class Diagram Generator (cdg)")
    parser.add_argument(
        "path",
        help="path to .csproj dir",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="path to output dir (default: .csproj dir)",
    )
    args = parser.parse_args()

    path: str = args.path
    output: str = args.output

    if output is None:
        output = path

    with open(
        os.path.join(output, f"{os.path.split(path)[1]}.cd.md"),
        "w",
        encoding="utf-8",
    ) as file:
        file.write(Project.parse(path).to_mermaid())
