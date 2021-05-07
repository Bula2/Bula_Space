import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    content = b""
    for entr in index:
        if "/" in entr.name:
            content += b"40000 "
            ford = entr.name[: entr.name.find("/")]
            content += ford.encode() + b"\0"
            sha_of = b""
            sha_of += oct(entr.mode)[2:].encode() + b" "
            ford1 = entr.name[entr.name.find("/")+1:]
            sha_of += ford1.encode() + b"\0"
            sha_of += entr.sha1
            sha_of_end = hash_object(sha_of, "tree", True)
            content += bytes.fromhex(sha_of_end)
        else:
            content += oct(entr.mode)[2:].encode() + b" "
            content += entr.name.encode() + b"\0"
            content += entr.sha1
    tree = hash_object(content, "tree", True)
    return tree

def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    timezone=(time.strftime("%z", time.gmtime()))
    if author is None:
        author = os.environ["GIT_AUTHOR_NAME"] + " " + os.environ["GIT_AUTHOR_EMAIL"]
    data = f"tree {tree}\n"
    if parent is not None:
        data += f"parent {parent}\n"
    data += f"author {author} {str(int(time.mktime(time.localtime())))} {timezone}\n" \
            f"committer {author} {str(int(time.mktime(time.localtime())))} {timezone}\n" \
            f"\n{message}\n"
    return hash_object(data.encode(), "commit", True)
