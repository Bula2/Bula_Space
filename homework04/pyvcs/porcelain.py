import os
import pathlib
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object, read_tree
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir,paths)

def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    tree = write_tree(gitdir, read_index(gitdir))
    com = commit_tree(gitdir, tree, message, author=author)
    return com


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    ref = get_ref(gitdir)
    if os.path.isfile(gitdir / ref):
        branch_head = open(gitdir / ref, "r")
        ref = branch_head.read()
        branch_head.close()
    fmt, old_content = read_object(ref, gitdir)
    old_content_s = old_content.decode()
    objects = find_tree_files(old_content_s[5:25], gitdir)
    project_dir = gitdir.absolute().parent
    for obj in objects:
        os.remove(project_dir / obj[0])
        par_path = pathlib.Path(obj[0]).parent
        while len(par_path.parents) > 0:
            os.rmdir(par_path)
            par_path = pathlib.Path(par_path).parent
    f_ref = open(gitdir / "HEAD", "w")
    f_ref.write(obj_name)
    f_ref.close()
    fmt, new_content = read_object(obj_name, gitdir)
    new_content_s = new_content.decode()
    objects = find_tree_files(new_content_s[5:25], gitdir)
    for obj in objects:
        par_cnt = len(pathlib.Path(obj[0]).parents)
        par_path = project_dir
        for par in range(par_cnt - 2, -1, -1):
            par_path /= pathlib.Path(obj[0]).parents[par]
            if not os.path.isdir(par_path):
                os.mkdir(par_path)
        fmt, obj_content = read_object(obj[1], gitdir)
        if fmt == "blob":
            pathlib.Path(project_dir / obj[0]).touch()
            f_blob = open(project_dir / obj[0], "w")
            f_blob.write(obj_content.decode())
            f_blob.close()
        else:
            os.mkdir(project_dir / obj[0])
