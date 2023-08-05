from datetime import timezone
from dateutil.parser import parse
from github import Github
from github.Branch import Branch
from github.ContentFile import ContentFile
from github.Repository import Repository
from hdsr_pygithub import constants
from hdsr_pygithub import exceptions
from pathlib import Path
from typing import List

import datetime
import logging


logger = logging.getLogger(__name__)


class GithubFileDownloader:
    """A wrapper around https://github.com/PyGithub/PyGithub. It uses a read-only github account
    token for interacting with hdsr github repos (see README.md)."""

    def __init__(
        self,
        repo_name: str,
        target_file: Path,
        branch_name: str = None,
        target_file_allowed_period_no_updates: datetime.timedelta = datetime.timedelta(weeks=52 * 1),
        personal_access_token: str = constants.GITHUB_HDSR_READ_ONLY_ACCOUNT_ACCESS_TOKEN,
        repo_organisation: str = constants.DEFAULT_GITHUB_ORGANISATION,
    ) -> None:
        self.repo_name = repo_name
        self.target_file = target_file
        self.branch_name = branch_name if branch_name else "main"
        self.target_file_allowed_period_no_updates = target_file_allowed_period_no_updates
        self.personal_access_token = personal_access_token
        self.repo_organisation = repo_organisation
        self._github_instance = None
        self._repo_instance = None
        self._target_file_content = None
        self.validate_constructor()

    def validate_constructor(self) -> None:
        assert (
            isinstance(self.personal_access_token, str) and self.personal_access_token
        ), f"github personal access token must be str {self.personal_access_token}"
        assert isinstance(self.target_file, Path), f"target_file {self.target_file} must be a Path"
        assert isinstance(self.target_file_allowed_period_no_updates, datetime.timedelta), (
            f"target_file_allowed_period_no_updates must be a datetime.timedelta "
            f"{self.target_file_allowed_period_no_updates}"
        )
        assert isinstance(self.repo_name, str) and self.repo_name, f"repo_name must be str {self.repo_name}"
        if self.repo_organisation:
            assert isinstance(self.repo_organisation, str), f"repo_organisation must be a str {self.repo_organisation}"

        available_branches = [branch.name for branch in self.repo_instance.get_branches()]
        if self.branch_name not in available_branches:
            raise exceptions.GithubBranchNotFound(msg=f"branch '{self.branch_name}' not found in {available_branches}")
        self.__check_target_file_is_recent_enough()

    @property
    def github_instance(self) -> Github:
        if self._github_instance is not None:
            return self._github_instance
        self._github_instance = Github(login_or_token=self.personal_access_token)
        return self._github_instance

    @property
    def repo_instance(self) -> Repository:
        if self._repo_instance is not None:
            return self._repo_instance
        repo_full_name = f"{self.repo_organisation}/{self.repo_name}" if self.repo_organisation else self.repo_name
        try:
            repo_instance = self.github_instance.get_repo(full_name_or_id=repo_full_name, lazy=False)
        except Exception as err:
            msg = f"can not create repo instance {repo_full_name} with user {self.github_instance.get_user().html_url}."
            if self.__public_repo_works_okay():
                msg += (
                    f" However, a (test) public repo (that should work) does work.. "
                    f"Does repo '{repo_full_name}' exist? err={err}"
                )
            else:
                msg += (
                    f" A (test) public repo (that should work) also does not work. "
                    f"Please check your personal access token, err={err}"
                )
            raise exceptions.GithubRepoInstanceError(msg=f"{msg}, err={err}")
        private_or_public = "private" if repo_instance.private else "public"
        logger.info(f"found {private_or_public} repo {repo_instance.html_url}")
        self._repo_instance = repo_instance
        return self._repo_instance

    @property
    def branch_instance(self) -> Branch:
        return self.repo_instance.get_branch(branch=self.branch_name)

    @property
    def target_file_content(self) -> ContentFile:
        """Get the start- and enddate (pandas Dataframe) for each PS based on the xml files (timeseries).
        This exercise is done in another github repo ('startenddate'). Here we try to download the latest version
        of the results (.csv) of that exercise. Why not use the locally cloned repo 'startenddate'? Well, it might
        be that that local repo is checkout to a branch other than main/master."""
        if self._target_file_content is not None:
            return self._target_file_content
        # download_url = f"https://www.github.com/{self.repo_instance.full_name}/{self.target_file.as_posix()}"
        # logger.info(f"preparing download github file {download_url}")
        branch_content_files = self.__get_branch_files_absolute_paths()
        self._target_file_content = self.__find_content_file(repo_content_files=branch_content_files)
        return self._target_file_content

    def __get_target_file_content_last_modified_date(self) -> datetime:
        """As file.last_modified (is file modification) is not the same as github_content_file.last_modified (is
        repo modification), we need to find the file in commits (within a branch) and then get the .last_modified."""
        all_branch_commits = self.repo_instance.get_commits(sha=self.branch_name)
        for commit in all_branch_commits:
            for file in commit.files:
                if self.target_file_content.sha == file.sha:
                    last_modified = file.last_modified
                    return parse(last_modified)
        raise exceptions.GithubFileNotFoundError(msg="this should not happen, could not find file in commits")

    def __check_target_file_is_recent_enough(self) -> None:
        """It is considered good practice to always check if the github file is not too old: just check last
        commit date."""
        last_modified_date = self.__get_target_file_content_last_modified_date()
        period_file_not_updated = datetime.datetime.now(timezone.utc) - last_modified_date.astimezone(timezone.utc)
        if period_file_not_updated > self.target_file_allowed_period_no_updates:
            msg = (
                f"Github file (name={self.target_file_content.name}) is too old. "
                f"\n File is {period_file_not_updated.days} days not updated, while allowed is "
                f"{self.target_file_allowed_period_no_updates.days} days: {self.target_file_content.html_url}"
            )
            raise exceptions.GithubFileTooOldError(msg=msg)
        logger.info(
            f"github file ({self.target_file_content.name}) is recent enough: not updated for "
            f"{period_file_not_updated.days} days while max allowed is "
            f"{self.target_file_allowed_period_no_updates.days} days"
        )

    def __public_repo_works_okay(self) -> bool:
        """"In case access to a github private repo does not work, we test if access to a public repo works.
        We use the repo 'https://github.com/PyGithub/PyGithub' (the one that we use here for: 'pip install PyGithub'
        and 'from github import Github'."""
        expected_url = "https://github.com/PyGithub/PyGithub"
        try:
            git = Github(login_or_token=self.personal_access_token)
            repo_instance = git.get_repo(full_name_or_id="PyGithub/PyGithub")
            assert repo_instance.html_url == expected_url
            logger.info(f"repo instance works for public repo {expected_url}")
            return True
        except Exception:  # noqa
            logger.error(f"repo instance does not works for public repo {expected_url}")
            return False

    def __get_branch_files_absolute_paths(self) -> List[ContentFile]:
        """
        Example
            this:
                from github import Repository

                repo = Repository(full_name="hdsr-mid/startenddate")
                __get_repo_files_absolute_path(repo=Repository(full_name=repo)
            returns:
                [
                    ContentFile(path=".gitignore"),
                    ContentFile(path="README.md"),
                    ContentFile(path="environment.yml"),
                    etc..
                    ContentFile(path="startenddate/__init__.py"),
                    etc..
                    ContentFile(path="data/input/corrected_caw_oppervlaktewater.csv"),
                    ContentFile(path="data/output/results/mwm_peilschalen_short.csv")
                    etc..
                ]
        """
        content_files = []
        # get root content files
        repo_root_dir = ""
        contents = self.repo_instance.get_contents(path=repo_root_dir, ref=self.branch_name)
        while contents:
            content = contents.pop(0)
            if content.type == "dir":
                # add subdir content files
                dir_contents = self.repo_instance.get_contents(path=content.path, ref=self.branch_name)
                contents.extend(dir_contents)
                continue
            if content.type == "file":
                content_files.append(content)
        return content_files

    def __find_content_file(self, repo_content_files: List[ContentFile]) -> ContentFile:
        # first, try exact match  based on whole filepath
        content_files = [x for x in repo_content_files if self.target_file.as_posix() in x.path]
        if len(content_files) == 1:
            content_file = content_files[0]
            logger.info(f"found exact match online: {content_file.path}")
            logger.debug(f"found file: {content_file.url} = url")
            logger.debug(f"found file: {content_file.html_url} = html_url")
            logger.debug(f"found file: {content_file.git_url} = git_url")
            logger.debug(f"found file: {content_file.download_url} = download_url")
            return content_file

        # secondly, try exact match based on filename (not path).
        content_files = [x for x in repo_content_files if x.name == self.target_file.name]
        if len(content_files) == 1:
            content_file = content_files[0]
            logger.info(f"found exact match online: {content_file.path}")
            logger.debug(f"found file: {content_file.url} = url")
            logger.debug(f"found file: {content_file.html_url} = html_url")
            logger.debug(f"found file: {content_file.git_url} = git_url")
            logger.debug(f"found file: {content_file.download_url} = download_url")
            return content_file

        default_error_msg = f"could not find file {self.target_file.name} in repo {self.repo_instance.name}"
        if len(content_files) > 1:
            default_error_msg += f', found >1 files with name {self.target_file.name} in repo")'
        raise exceptions.GithubFileNotFoundError(msg=default_error_msg)
