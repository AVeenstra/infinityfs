#!/usr/bin/env python

from __future__ import with_statement

from errno import EACCES
from sys import argv, exit

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn

maxpathlength = 2000
now = time.time()
st = {}
st['st_mode']   = 0333
st['st_ino']    = 0
st['st_dev']    = 0
st['st_nlink']  = 1
st['st_uid']    = 1000
st['st_gid']    = 1000
st['st_size']   = 1024
st['st_atime']  = now
st['st_mtime']  = now
st['st_ctime']  = now
st['st_blocks'] = (int) ((st['st_size'] + 511) / 512)
folders = ['.','..'] + [str(chr(x)) for x in range(ord('A'),ord('Z')+1)]

class InfinityFS(LoggingMixIn, Operations):
    def __init__(self):
        pass

    def access(self, path, mode):
        if maxpathlength < len(path):
            raise FuseOSError(EACCES)

    chmod = None
    chown = None
    create = None
    flush = None
    fsync = None

    def getattr(self, path, fh=None):
        if maxpathlength < len(path):
            raise FuseOsError(ENOENT)
        return st

    getxattr = None
    link = None
    listxattr = None
    mkdir = None
    mknod = None
    open = None
    read = None

    def readdir(self, path, fh):
        if maxpathlength < len(path):
            raise FuseOsError(ENOENT)
        if maxpathlength < len(path) - 2:
            return ['.','..']
        return folders

    readlink = None
    release = None
    rename = None
    rmdir = None
    statfs = None
    symlink = None
    truncate = None
    unlink = None
    utimens = None


if __name__ == '__main__':
    if len(argv) != 2:
        print('usage: %s <mountpoint>' % argv[0])
        exit(1)

    fuse = FUSE(InfinityFS(), argv[1], foreground=True)

