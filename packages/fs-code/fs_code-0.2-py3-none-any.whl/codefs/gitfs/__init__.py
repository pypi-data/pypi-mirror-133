"""
`RepoFS` is a read-only filesystem which uses <a target="_blank" href="https://www.dulwich.io/">dulwich</a> to download a
Git archive.

Usage with <a target="_blank" href="https://docs.pyfilesystem.org/en/latest/openers.html">FS URL</a>:

```python
import fs

repo_fs = fs.open_fs("gitfs://https://gitlab.com/dAnjou/fs-code.git")
readme = repo_fs.open("main/README.md")
print(readme.read())
```

Usage with <a target="_blank" href="https://www.dulwich.io/docs/api/dulwich.client.html">dulwich</a> client:

```python
from urllib.parse import urlparse
from dulwich.client import HttpGitClient

url = urlparse("https://gitlab.com/dAnjou/fs-code.git")
repo_fs = RepoFS(HttpGitClient.from_parsedurl(url), url.path)
readme = repo_fs.open("main/README.md")
print(readme.read())
```
"""

from io import BytesIO
from typing import Mapping, Optional

from dulwich import porcelain
from dulwich.client import FetchPackResult, GitClient
from dulwich.porcelain import NoneStream
from dulwich.refs import LOCAL_BRANCH_PREFIX, LOCAL_TAG_PREFIX
from dulwich.repo import MemoryRepo
from fs.base import FS
from fs.subfs import SubFS
from fs.tarfs import ReadTarFS
from fs.wrap import read_only, WrapReadOnly

from codefs.core import RefFS, AbstractArchiveFetcher

__all__ = [
    "RepoFS",
]

__pdoc__ = {
    "opener": False,
}


class RepoFS(SubFS[WrapReadOnly[RefFS]]):
    """"""
    def __init__(self, client: GitClient, path: str):
        """
        Arguments
        ---------
        client : dulwich.client.GitClient
            or any subclass of <a target="_blank" href="https://www.dulwich.io/docs/api/dulwich.client.html#dulwich.client.GitClient">`GitClient`</a>
        path : str
            a path to the repository
        """
        super().__init__(read_only(RefFS(ArchiveFetcher(client, path))), "/")


class ArchiveFetcher(AbstractArchiveFetcher):
    def __init__(self, client: GitClient, path: str):
        self._client = client
        self._path = path
        self._repo = MemoryRepo()  # type: ignore
        self._cache: Optional[bytes] = None

    @staticmethod
    def get_ref(refs: Mapping[bytes, bytes], ref: bytes) -> bytes:
        if sha := refs.get(ref):
            return sha
        branch = refs.get(LOCAL_BRANCH_PREFIX + ref)
        tag = refs.get(LOCAL_TAG_PREFIX + ref)
        if branch and not tag:
            return branch
        if tag and not branch:
            return tag
        raise RuntimeError(f"{ref!r} is both, a branch and a tag")

    def __call__(self, ref: str) -> FS:
        if not self._cache:
            result: FetchPackResult = self._client.fetch(self._path, self._repo, depth=1)  # type: ignore
            committish = self.get_ref(result.refs, ref.encode())
            data = BytesIO()
            porcelain.archive(
                self._repo,
                committish=committish,
                outstream=data,
                errstream=NoneStream()
            )  # type: ignore
            data.seek(0)
            self._cache = data.getvalue()
        return ReadTarFS(BytesIO(self._cache))  # type: ignore
