from .commit_parser import parser_from_message


def commit_to_dict(commit):
    """Convert given Commit Instance in structered Object"""
    return {
        "hexsha": str(commit.hexsha),
        "summary": str(commit.summary),
        "message": parser_from_message(str(commit.message)),
        "parents": commit.parents,
        "author": {"name": str(commit.author.name), "email": str(commit.author.email)},
        "committer": {
            "name": str(commit.committer.name),
            "email": str(commit.committer.email),
        },
        "authored_datetime": str(commit.authored_datetime),
        "authored_date": int(commit.authored_date),
        "committed_date": int(commit.committed_date),
        "count": int(commit.count()),
        "size": int(commit.size),
    }
