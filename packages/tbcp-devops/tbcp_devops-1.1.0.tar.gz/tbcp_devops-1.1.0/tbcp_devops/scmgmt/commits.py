"""
Working with Git Commits object

Reference:
- https://gitpython.readthedocs.io/en/stable/tutorial.html#the-commit-object
- https://gitpython.readthedocs.io/en/stable/tutorial.html#understanding-objects
"""

import sys
import git
from .repository import Repository


class Commits(Repository):
    """Inherits the self.repo instance"""

    def set_commit(message):
        try:
            repo = super().get_repo()
            repo.git.commit(m=message)
        except git.InvalidGitRepositoryError as error:
            print(f"Oops! That was not a valid Git repository {format(error)}")
            raise
        except git.GitCommandError as error:
            print(f"Oops! That was not a valid Git command {format(error)}")
            raise
        except ValueError:
            print(f"That is not a string. Try again!: {format(sys.exc_info()[0])}")
            raise
        except BaseException:
            print(f"Unexpected error: {format(sys.exc_info()[0])}")
            raise

    def commit_to_dict(self, commit):
        """Convert given Commit Instance in structered Object"""
        return {
            "hexsha": str(commit.hexsha),
            "tree": {"type": str(commit.tree.type)},
            "summary": str(commit.summary),
            "message": str(commit.message),
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

    def get_recent_commit(self) -> dict:
        """Return the latest commit of the repository"""
        repo = super().get_repo()
        return self.commit_to_dict(repo.head.commit)

    def get_list_of_commits(self, head="main", max_count=50, skip=0) -> list:
        repo = super().get_repo()

        list_of_commits = []
        for commit in repo.iter_commits(head, max_count=max_count, skip=skip):
            list_of_commits.append(self.commit_to_dict(commit))

        return list_of_commits

    def get_commit_by_hexsha(self, hexsha: str):
        """
        Provide a list of commits. Default: max=50, head=main, skip=0

        - commit.hexsha
        - commit.summary
        - commit.author.name
        - commit.author.email
        - commit.authored_datetime
        - commit.count()
        - commit.size
        """

        commit_of_hexsha = ""
        list_of_commits = self.get_list_of_commits()
        for commit in list_of_commits:
            if hexsha == commit["hexsha"]:
                commit_of_hexsha = commit

        return commit_of_hexsha

    def commit_message(
        self, type_of: str, description: str, breaking=False, breaking_msg="", scope="", bodies=[""], footer=""
    ):
        """"""
        # Commits MUST be prefixed with a type, which consists of a noun, feat, fix, etc.,
        # followed by the OPTIONAL scope,
        # OPTIONAL !, and REQUIRED terminal colon and space.
        #
        # Breaking changes MUST be indicated in the type/scope prefix of a commit, or as an entry in the footer.
        #
        # If included as a footer, a breaking change MUST consist of the uppercase text BREAKING CHANGE,
        # followed by a colon, space, and description,
        # e.g., BREAKING CHANGE: environment variables now take precedence over config files.
        breaking_sign = "!" if breaking else ""
        #
        # The type `feat` MUST be used when a commit adds a new feature to your application or library.
        # The type `fix` MUST be used when a commit represents a bug fix for your application.
        #
        # Types other than feat and fix MAY be used in your commit messages, e.g., docs: updated ref docs.
        type_of = (
            type_of
            if type_of.lower()
            in ["fix", "feat", "build", "chore", "ci", "docs", "style", "refactor", "perf", "test", "revert"]
            else ""
        )
        #
        # A scope MAY be provided after a type.
        # A scope MUST consist of a noun describing a section of the codebase surrounded by parenthesis, e.g., fix(parser):
        scope = "(" + scope + ")" if scope else ""
        #
        # A description MUST immediately follow the colon and space after the type/scope prefix.
        # The description is a short summary of the code changes, e.g., fix: array parsing issue when multiple spaces were contained in string.
        #
        # A longer commit body MAY be provided after the short description, providing additional contextual information about the code changes.
        # The body MUST begin one blank line after the description.
        #
        # A commit body is free-form and MAY consist of any number of newline separated paragraphs.
        body = []
        if isinstance(bodies, str) and bodies:
            body = "\n\n" + bodies
        elif isinstance(bodies, list) and len(bodies) == 1:
            body = "\n\n" + str(bodies[0])
        elif isinstance(bodies, list) and len(bodies) > 1:
            for sep_body in bodies:
                body.append("\n\n" + sep_body + "\n")
        #
        # If included in the type/scope prefix, breaking changes MUST be indicated by a ! immediately before the :.
        # If ! is used, BREAKING CHANGE: MAY be omitted from the footer section,
        # and the commit description SHALL be used to describe the breaking change.
        breaking_msg = "\n\nBREAKING CHANGE: " if breaking and footer else ""
        #
        # One or more footers MAY be provided one blank line after the body.
        # Each footer MUST consist of a word token, followed by either a :<space> or <space># separator,
        # followed by a string value (this is inspired by the git trailer convention).
        #
        # A footer’s token MUST use - in place of whitespace characters,
        # e.g., Acked-by (this helps differentiate the footer section from a multi-paragraph body).
        # An exception is made for BREAKING CHANGE, which MAY also be used as a token.
        #
        # A footer’s value MAY contain spaces and newlines,
        # and parsing MUST terminate when the next valid footer token/separator pair is observed.
        footer_space = "\n\n" if not breaking else ""
        footer = footer_space + footer if footer else ""

        row_header = type_of + scope + breaking_sign + ": " + description
        row_body = body
        rwo_footer = breaking_msg + footer

        message = " ".join(filter(None, [row_header, row_body, rwo_footer]))

        return message


#     def catch_commit_from_hook(self, repo_instance):
#         """Catch a commit message"""
#         self.repo_instance = repo_instance

#         self.repo_instance.index.commit('Initial commit.')

#     def take_commit_message(self, repo_instance, commit_message):
#         """Provide a commit message"""
#         self.repo_instance = repo_instance
#         self.commit_message = commit_message

#         self.repo_instance.index.commit('Initial commit.')
