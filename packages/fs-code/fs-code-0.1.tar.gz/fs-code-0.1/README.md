# fs-code

![pipeline status][pipeline status] ![3.8 coverage][3.8 coverage] ![3.10 coverage][3.10 coverage]

[PyFilesystems](https://www.pyfilesystem.org/) for GitLab, GitHub, and Git.

---

## Installation

TODO

## Usage

### with <a target="_blank" href="https://docs.pyfilesystem.org/en/latest/openers.html">FS URL</a>

```python
import fs

user_fs = fs.open_fs("gitlab://?user=dAnjou")
readme = user_fs.open("fs-code/main/README.md")
print(readme.read())
```

### with class

```python
from gitlab import Gitlab
from codefs.gitlabfs import UserFS

user_fs = UserFS(Gitlab(), user="dAnjou")
readme = user_fs.open("fs-code/main/README.md")
print(readme.read())
```

[pipeline status]: https://gitlab.com/dAnjou/fs-code/badges/main/pipeline.svg
[3.8 coverage]: https://gitlab.com/dAnjou/fs-code/badges/main/coverage.svg?job=test%3A%20%5Bpython%3A3.8%5D&key_text=3.8+coverage&key_width=90
[3.10 coverage]: https://gitlab.com/dAnjou/fs-code/badges/main/coverage.svg?job=test%3A%20%5Bpython%3A3.10%5D&key_text=3.10+coverage&key_width=90
