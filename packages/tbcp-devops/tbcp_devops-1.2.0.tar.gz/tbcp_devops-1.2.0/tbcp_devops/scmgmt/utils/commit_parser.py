""""""
import re


def get_header(row_header: str):

    if ":" in row_header:
        header_split = row_header.split(":")
        header_left = header_split[0].lstrip().rstrip()

        breaking = bool("!" in header_left)

        description = header_split[-1].lstrip().rstrip()

        if "(" in header_left:
            scope = re.search("\(+[a-zA-Z 0-9]*\)+", header_left)
            scope = scope.group().replace("(", "").replace(")", "")

            return {"type": header_left, "scope": scope, "description": description, "breaking": breaking}

        return {"type": header_left, "description": description, "breaking": breaking}
    else:
        return {"description": row_header}


def get_footer(row_footer: str):

    breaking = bool("BREAKING" in row_footer)

    return {"description": row_footer, "breaking": breaking}


def get_body(row_body: str):

    breaking = bool("BREAKING" in row_body)

    return {"description": row_body, "breaking": breaking}


def parser_from_message(message: str) -> str:

    row_of_commit = message.lstrip().rstrip().split("\n\n")
    if len(row_of_commit) >= 1:
        header = get_header(row_of_commit[0])
        row_of_commit.remove(row_of_commit[0])
        if row_of_commit:
            footer = get_footer(row_of_commit[-1])
            row_of_commit.remove(row_of_commit[-1])

            body = get_body(row_of_commit)

            if row_of_commit:
                return {"header": header, "body": body, "footer": footer, "text": message}

            return {"header": header, "footer": footer, "text": message}
        else:
            return {"header": header, "text": message}

    # iter = 0
    # body_space = []
    # for line in row_of_commit:
    #     if line == "":
    #         body_space.append(iter)
    #     iter += 1
