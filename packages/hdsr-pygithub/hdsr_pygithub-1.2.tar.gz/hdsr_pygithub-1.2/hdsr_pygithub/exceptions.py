class GithubFileTooOldError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class GithubFileNotFoundError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class GithubBranchNotFound(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class GithubRepoInstanceError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)
