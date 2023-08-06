""""""
import re


def get_header(row_header: str):
    header_split = row_header.split(":")
    header_left = header_split[0].lstrip().rstrip()

    breaking = header_left.endswith("!")
    header_left = header_left.replace("!", "")

    scope = re.search("\(+[a-zA-Z 0-9]*\)+", header_left)
    scope = scope.group().replace("(", "").replace(")", "")
    header_left = header_left.replace("(" + scope + ")", "")

    description = header_split[-1].lstrip().rstrip()

    header = {"type_of": header_left, "scope": scope, "breaking": breaking, "description": description}

    return header


def get_footer(row_footer: str):
    return


def get_body(row_body: str):
    return


def parser(commit: str) -> str:
    row_of_commit = commit.lstrip().rstrip().split("\n")

    row_header = row_of_commit[0]
    header = get_header(row_header)
    row_of_commit.remove(row_header)

    # iter = 0
    # body_space = []
    # for line in row_of_commit:
    #     if line == "":
    #         body_space.append(iter)
    #     iter += 1

    return {"header": header}
