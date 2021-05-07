import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    header = f"{fmt} {len(data)}\0"
    sum = header.encode() + data
    sha = hashlib.sha1(sum).hexdigest()
    if write == True:
        gitdir = repo_find()
        if (not os.path.exists(gitdir / "objects" / sha[:2])):
            pathlib.Path(gitdir / "objects" / sha[:2]).mkdir()
        if (not os.path.exists(gitdir / "objects" / sha[:2] / sha[2:])):
            pathlib.Path(gitdir / "objects" / sha[:2] / sha[2:]).touch()
        with (pathlib.Path(gitdir / "objects" / sha[:2]) / sha[2:]).open("wb") as f:
            f.write(zlib.compress(sum))
            f.close()
    return (sha)


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    obj_name_len = len(obj_name)
    if (obj_name_len > 3 and obj_name_len < 41):
        a = []
        pth = pathlib.Path(gitdir / "objects")
        fl, dir = None, None
        for dirpath, dirnames, filenames in os.walk(pth):
            for name in dirnames:
                dir = os.path.join(dirpath, name)
                dir = os.path.basename(dir)
            for file in filenames:
                fl = os.path.join(dirpath, file)
                fl = os.path.basename(fl)
                if obj_name in (dir + fl)[0:(obj_name_len + 1)]:
                    a.append(dir + fl)
        if (len(a) == 0):
            raise AssertionError(f"Not a valid object name {obj_name}")
        return (a)
    raise AssertionError(f"Not a valid object name {obj_name}")


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    path = str(gitdir) + "/" + "objects" + "/" + obj_name[:2] + "/" + obj_name[2:]
    return (path)


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    path = pathlib.Path(gitdir / "objects" / sha[:2] / sha[2:])
    with path.open("rb") as f:
        data = zlib.decompress(f.read())
        a, b = data[0:4].decode(), data[8:]
        f.close()
    return (a, b)


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    result= []
    data=data[1:]
    while len(data)>0:
        mode = data[:6].decode()
        zero = data.find(b"\00")
        if mode=="100644":
            name=data[7:zero]
            sha=data[zero+1:zero+21].hex()
            result.append((100644, name.decode(), sha))
            data=data[zero+21:]
        else:
            name=data[6:zero]
            sha=data[zero+1:zero+21].hex()
            result.append((40000, name.decode(), sha))
            data=data[zero+21:]
    return result


def cat_file(obj_name: str, pretty: bool = True) -> None:
    gitdir=repo_find()
    fmt, data =read_object(obj_name, gitdir)

    if fmt=="blob" or fmt == "commit":
        if pretty:
            print(data.decode())
        else:
            print(data)
    else:
        result=""
        if pretty:
            for file in read_tree(data):
                result += str(file[0]).zfill(6) + " "
                if file[0]==100644:
                    result+="blob "
                else:
                    result+="tree "
                result += str(file[2]) + "\t"
                result += str(file[1]) + "\n"
            print(result)
        else:
            for file in read_tree(data):
                print(file[2])


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    fmt, content = read_object(tree_sha, gitdir)
    objects = read_tree(content)
    arr = []
    for i in objects:
        if i[0] == 100644:
            arr.append((i[1], i[2]))
        else:
            sub_objects = find_tree_files(i[2], gitdir)
            for j in sub_objects:
                arr.append((i[1] + "/" + j[0], j[1]))
    return arr


def commit_parse(raw: bytes, start: int = 0, dct=None):
    pass
