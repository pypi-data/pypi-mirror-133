import logging
from pathlib import PurePosixPath
from typing import TypeVar, Callable, Generic, Mapping, List, Tuple, Protocol, Union

from fs.base import FS
from fs.errors import Unsupported, ResourceNotFound
from fs.memoryfs import MemoryFS
from fs.mountfs import MountFS
from fs.path import abspath, normpath
from fs.subfs import SubFS
from fs.wrap import read_only, WrapReadOnly
from schema import And, Use  # type: ignore

__all__ = [
    'NamespaceFS',
    'RefFS',
    'AbstractArchiveFetcher',
    'AbstractReposFetcher',
]

Repository = TypeVar('Repository', covariant=True)


class AbstractReposFetcher(Protocol[Repository]):
    def get_repo(self, name: str) -> Repository:
        ...

    def get_repos(self) -> Mapping[str, Repository]:
        ...


class AbstractArchiveFetcher(Protocol):
    def __call__(self, ref: str) -> FS:
        ...


class NamespaceFS(SubFS[WrapReadOnly[MountFS]]):
    def __init__(self, repos_fetcher: AbstractReposFetcher[Repository],
                 archive_fetcher: Callable[[Repository], AbstractArchiveFetcher]):
        self.repo_fs = RepoFS(repos_fetcher, archive_fetcher)
        super().__init__(read_only(self.repo_fs), "/")


def _is_root(path: str) -> bool:
    return abspath(normpath(path)) == "/"


class RepoFS(Generic[Repository], MountFS):
    def __init__(self, repos_fetcher: AbstractReposFetcher[Repository],
                 archive_fetcher: Callable[[Repository], AbstractArchiveFetcher]) -> None:
        super().__init__()
        self.repos_fetcher = repos_fetcher
        self.archive_fetcher = archive_fetcher

    def mount(self, path: str, fs: Union[FS, str]) -> None:
        if path not in [m.strip("/") for m, _ in self.mounts]:
            super().mount(path, fs)

    def _delegate(self, path: str) -> Tuple[FS, str]:
        try:
            if not _is_root(path):
                mount_point = repo_name = PurePosixPath(abspath(normpath(path))).parts[1]
                repo: Repository = self.repos_fetcher.get_repo(repo_name)
                self.mount(mount_point, read_only(RefFS(self.archive_fetcher(repo))))
        except Exception as e:
            logging.exception("failed to mount repo")
            raise ResourceNotFound(path, e)
        fs, path = super()._delegate(path)
        return fs, path

    def listdir(self, path: str) -> List[str]:
        if _is_root(path):
            repos: Mapping[str, Repository] = self.repos_fetcher.get_repos()
            for name, repo in repos.items():
                self.mount(name, read_only(RefFS(self.archive_fetcher(repo))))
        return super().listdir(path)


class RefFS(MountFS):
    def __init__(self, fetch_archive: AbstractArchiveFetcher) -> None:
        super().__init__()
        self.fetch_archive = fetch_archive

    def _reset(self) -> None:
        self.mounts = []
        self.default_fs = MemoryFS()

    def _delegate(self, path: str) -> Tuple[FS, str]:
        try:
            if not _is_root(path):
                mount_point = ref = PurePosixPath(abspath(normpath(path))).parts[1]
                self.mount(mount_point, self.fetch_archive(ref))
        except Exception as e:
            self._reset()
            logging.exception("failed to mount repo archive")
            raise ResourceNotFound(path, e)
        fs, path = super()._delegate(path)
        if fs is not self.default_fs:
            self._reset()
        return fs, path

    def listdir(self, path: str) -> List[str]:
        if _is_root(path):
            raise Unsupported(path, msg='listing refs is too expensive')
        return super().listdir(path)


def Str() -> And:
    return And(str, len, error="must be non-empty string")


def Float() -> Use:
    return Use(float)


def Int() -> Use:
    return Use(int)


def Bool() -> Use:  # todo: no cover, because I'm not testing it yet
    return Use(lambda value: {"true": True, "false": False}[value.lower()])
