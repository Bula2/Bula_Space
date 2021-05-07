import os
import pathlib
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir, paths)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    commit = commit_tree(gitdir, write_tree(gitdir, read_index(gitdir)), message, author=author)
    if is_detached(gitdir):
        ref = gitdir / "HEAD"
    else:
        ref = pathlib.Path(get_ref(gitdir))
    f = open(gitdir / ref, "w")
    f.write(commit)
    f.close()
    return commit


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    gref = get_ref(gitdir)
    if os.path.isfile(gitdir / gref):
        branch_head = open(gitdir / gref, "r")
        gref = branch_head.read()
        branch_head.close()
    fmt, content_0 = read_object(gref, gitdir)
    old_content_s = content_0.decode()
    objects = find_tree_files(old_content_s[5:25], gitdir)
    dir = gitdir.absolute().parent
    for obj in objects:
        os.remove(dir / obj[0])
        par_path = pathlib.Path(obj[0]).parent
        while len(par_path.parents) > 0:
            os.rmdir(par_path)
            par_path = pathlib.Path(par_path).parent
    f_gref = open(gitdir / "HEAD", "w")
    f_gref.write(obj_name)
    f_gref.close()
    fmt, content = read_object(obj_name, gitdir)
    content1 = content.decode()
    objects = find_tree_files(content1[5:25], gitdir)
    for obj in objects:
        par_count = len(pathlib.Path(obj[0]).parents)
        par_path = dir
        for par in range(par_count - 2, -1, -1):
            par_path /= pathlib.Path(obj[0]).parents[par]
            if not os.path.isdir(par_path):
                os.mkdir(par_path)
        fmt, obj_content = read_object(obj[1], gitdir)
        if fmt == "blob":
            pathlib.Path(dir / obj[0]).touch()
            blob = open(dir / obj[0], "w")
            blob.write(obj_content.decode())
            blob.close()
        else:
            os.mkdir(dir / obj[0])