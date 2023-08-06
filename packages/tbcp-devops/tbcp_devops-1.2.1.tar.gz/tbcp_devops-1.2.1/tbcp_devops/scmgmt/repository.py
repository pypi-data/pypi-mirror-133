"""
Working with Git Repositories

- Checking if there are any changes
- Get a diff of changes

Refernences:
- https://gitpython.readthedocs.io/en/stable/tutorial.html#meet-the-repo-type
- https://gitpython.readthedocs.io/en/stable/tutorial.html#initializing-a-repository
"""

import sys
import git
from git.refs.head import HEAD
from ._defaults import *
from ._errors import *


class Repository:
    """"""

    def __init__(self, repo_dir=DEF_REPO_PATH) -> None:
        """Gets the repository instance inherited by super()

        Default: repo_dir = './'
        """
        try:
            self.repo = git.Repo(str(repo_dir))
        except git.InvalidGitRepositoryError as error:
            print(ERR_INVALID_REPO + format(error))
            raise
        except git.GitCommandError as error:
            print(ERR_GIT_COMMAND + format(error))
            raise
        except git.GitCommandNotFound as error:
            print(ERR_GIT_COMMAND_NOT_FOUND + format(error))
            raise
        except git.GitError as error:
            print(ERR_GIT + format(error))
            raise
        except ValueError as error:
            print(ERR_VALUE + format(error))
            raise
        except BaseException:
            print(ERR_BASEEXEC + format(sys.exc_info()[0]))
            raise

    def get_repo(self):
        return self.repo

    def is_repo_bare(self) -> bool:
        """Return True if Repository Type is Bare"""
        return bool(self.repo.bare)

    def get_description(self) -> str:
        """Return the description of the current repository"""
        return str(self.repo.description)

    def has_separate_working_tree(self) -> bool:
        """Return boolean if the repository has a separate working tree"""
        return bool(self.repo.has_separate_working_tree())

    def get_repository_dir(self) -> str:
        """Return a list of known directories of the repository"""

        commun = str(self.repo.common_dir)
        working_tree = str(self.repo.working_tree_dir)
        working_dir = str(self.repo.working_dir)
        git_repo = str(self.repo.git_dir)

        if commun is working_dir or git_repo and not self.has_separate_working_tree():
            return commun
        elif commun is not working_tree and self.has_separate_working_tree():
            return working_tree

    # def get_alternates(self) -> list:
    #     """List Alternates"""
    #     return self.repo.alternates

    # def get_cmd_wrapper_type(self):
    #     """Provide Git Command Wrapper Type"""
    #     return format(self.repo.GitCommandWrapperType)

    def get_head(self) -> HEAD:
        """Return the head of the current repository"""
        return self.repo.head

    def get_heads(self) -> list:
        """Return the heads of the current repository"""
        list_heads = []
        for head in self.repo.heads:
            if head:
                list_heads.append({"heads": format(head)})

        return list_heads

    def add_files(self, list_files: list, all_files=False):

        if all_files:
            self.repo.index.add(all=True)
            return "All files added"
        else:
            self.repo.index.add(list_files)
            return "Selected files added"

    def stage_all_files(self):
        """"""
        self.repo.git.add(A=True)

    def has_changed_files(self) -> bool:
        """Return True if the repository has changed files"""
        return bool(self.repo.is_dirty(untracked_files=True))

    def lists_changed_files(self, where="unstaged") -> bool:
        """Return True if the repository has changed files"""
        if where is "unstaged":
            return [item.a_path for item in self.repo.index.diff(None)]
        elif where is "staged":
            return [item.a_path for item in self.repo.index.diff(self.repo.head.commit)]

    def lists_untracked_files(self) -> list:
        """Provide a list of the files to stage"""
        return list(self.repo.untracked_files)

    def get_diff(self):
        """Return the difference since the last commit"""
        return self.repo.git.diff(self.repo.head.commit.tree)

    def checkout(self) -> None:
        self.repo.head.checkout()

    def pull(self) -> None:
        self.repo.git.pull("origin", self.repo.head)

    def push(self, from_head="origin") -> None:
        self.repo.git.push("--set-upstream", from_head, self.repo.head)

    def list_remote(self) -> list:
        """Return the remote values of the current repository"""
        list_remotes = []
        for remote in self.repo.remotes:
            if remote:
                list_remotes.append({"url": format(remote.url), "name": format(remote.name)})

        return list_remotes

    def set_new_remote_origin(self, remote_url, remote_name="origin"):
        """Create a new remote"""

        return self.repo.create_remote(remote_name, url=remote_url)

    def pull_from_remote(self):
        """Pull from remote repo"""

        return self.repo.remotes.origin.pull()

    def push_to_remote(self):
        """Push changes"""
        return self.repo.remotes.origin.push()

    def delete_remote(self, remote_name="origin"):
        """Delete a remote"""
        # Reference a remote by its name as part of the object
        # print(f'Remote name: {repo.remotes.origin.name}')
        # print(f'Remote URL: {repo.remotes.origin.url}')

        return self.repo.delete_remote(remote_name)

    # def init(self, init_repo_name):
    #     """git init new_repo"""
    #     self.init_repo_name = init_repo_name

    #     self.repo_instance.init(self.init_repo_name)

    # def clone(self, remote_repo, local_path='./'):
    #     """Clone a Repository"""
    #     self.remote_repo = remote_repo
    #     self.local_path = local_path

    #     self._clone_from_url(self.remote_repo, self.local_path )
    #     self._clone_from_local(self.remote_repo, self.local_path)

    # def _clone_from_url(self, repo_url, repo_path):
    #     """Check out via HTTPS or clone via ssh (will use default keys)"""
    #     self.repo_url = repo_url
    #     self.repo_path = repo_path

    #     self.repo_instance.clone_from(self.repo_url, self.repo_path)

    # def _clone_from_local(self, repo_path, new_path):
    #     """Load existing local repo, Create a copy of the existing repo"""
    #     self.repo_path = repo_path
    #     self.new_path = new_path

    #     local_repo = self.repo_instance(self.repo_path)
    #     local_repo.clone(self.new_path)
