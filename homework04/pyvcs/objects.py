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
    if len(obj_name) not in range(4, 41) or not os.path.isdir(gitdir / "objects" / obj_name[0:2]):
        raise AssertionError(f"Not a valid object name {obj_name}")
    current_dir = gitdir / "objects" / obj_name[0:2]
    end = obj_name[2:]
    res = []
    for files in os.listdir(current_dir):
        if os.path.isfile(current_dir / files) and files == end or files[0:len(end)] == end:
            res.append(obj_name[0:2] + files)
    if len(res) == 0:
        raise AssertionError(f"Not a valid object name {obj_name}")
    return res

def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    return resolve_object(obj_name, gitdir)[0]


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    path = find_object(sha, gitdir)
    file = open(gitdir / "objects" / path[0:2] / path[2:], "rb")
    data = zlib.decompress(file.read())
    start, end = data.find(b" "), data.find(b"\x00")
    length = int(data[start:end].decode("ascii"))
    content = data[end + 1:]
    fmt = data[:start].decode()
    file.close()
    return fmt, content


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    result = []
    while len(data) > 0:
        mode = data[:6].decode()
        zero = data.find(b"\00")
        if mode == "100644":
            name = data[7:zero]
            sha = data[zero + 1:zero + 21].hex()
            result.append((100644, name.decode(), sha))
            data = data[zero + 21:]
        else:
            name = data[6:zero]
            sha = data[zero + 1:zero + 21].hex()
            result.append((40000, name.decode(), sha))
            data = data[zero + 21:]
    return result


def cat_file(obj_name: str, pretty: bool = True) -> None:
    gitdir=repo_find()
    fmt, data =read_object(obj_name, gitdir)
    if fmt=="blob" or fmt == "commit":
        print(data.decode())
    else:
        result=""
        for file in read_tree(data):
            result += str(file[0]).zfill(6) + " "
            if file[0]==100644:
                result+="blob "
            else:
                result+="tree "
            result += file[2] + "\t"
            result += file[1] + "\n"
        print(result)


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
    ...