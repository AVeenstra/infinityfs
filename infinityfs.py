#!/usr/bin/env python

from __future__ import with_statement

from errno import EACCES
from sys import argv, exit
import time
from fuse import FUSE, FuseOSError, Operations, LoggingMixIn

maxpathlength = 2000
now = time.time()
st = {}
st['st_mode']   = 16877
st['st_ino']    = 0
st['st_dev']    = 0
st['st_nlink']  = 1
st['st_uid']    = 1000
st['st_gid']    = 1000
st['st_size']   = 4096
st['st_atime']  = now
st['st_mtime']  = now
st['st_ctime']  = now
st['st_blocks'] = (int) ((st['st_size'] + 511) / 512)

allchars = [
        str(chr(x)) for x in range(ord('A'),ord('Z')+1)
    ] + [
        str(chr(x)) for x in range(ord('a'),ord('z')+1)
    ] + [
        str(x) for x in "'!@#$%()[]{};-+"
    ]

folders = ['.','..'] + allchars

class InfinityFS(LoggingMixIn, Operations):
    def __init__(self):
        pass

    def access(self, path, mode):
        #print("access of path: \"%s\"" % path)
        if maxpathlength < len(path):
            raise FuseOSError(EACCES)

    chmod = None
    chown = None
    create = None
    flush = None
    fsync = None

    def getattr(self, path, fh=None):
        #print("getattr of path: \"%s\"" % path)
        if maxpathlength < len(path):
            #print("  error")
            raise FuseOsError(ENOENT)
        #print("  returning st")
        return st

    getxattr = None
    link = None
    listxattr = None
    mkdir = None
    mknod = None
    open = None
    read = None

    def readdir(self, path, fh):
        #print("readdir of path: \"%s\"" % path)
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

