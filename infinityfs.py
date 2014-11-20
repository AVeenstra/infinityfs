#!/usr/bin/env python

from __future__ import with_statement

from errno import EACCES
from sys import argv, exit
import os
from fuse import FUSE, FuseOSError, Operations, LoggingMixIn

maxpathlength = 2000

allchars = [
        str(chr(x)) for x in range(ord('A'),ord('Z')+1)
    ] + [
        str(chr(x)) for x in range(ord('a'),ord('z')+1)
    ] + [
        str(x) for x in range(10)
    ] + [
        str(x) for x in "'!@#$%()[]{};-+"
    ]

folders = ['.','..'] + allchars

class InfinityFS(LoggingMixIn, Operations):
    def __init__(self,path,f):
        stos = os.lstat(path)
        self.st = dict((key, getattr(stos, key)) for key in ('st_atime', 'st_ctime',
            'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
        stv = os.statvfs(path)
        self.stv = dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))
        self.file = f
        stf = os.lstat(f)
        self.fileAttr = dict((key, getattr(stf, key)) for key in ('st_atime', 'st_ctime',
            'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def access(self, path, mode):
        #print("access of path: \"%s\"" % path)
        if maxpathlength < len(path):
            raise FuseOSError(EACCES)

    def getattr(self, path, fh=None):
        #print("getattr of path: \"%s\"" % path)
        if maxpathlength < len(path):
            #print("  error")
            raise FuseOsError(ENOENT)
        #print("  returning st")
        if maxpathlength - 17 < len(path):
            return self.fileAttr
        return self.st

    def read(self, path, size, offset, fh):
        f = os.open(self.file,os.O_RDONLY)
        os.lseek(f,offset, 0)
        buf = os.read(f,size)
        os.close(f)
        return buf

    def readdir(self, path, fh):
        #print("readdir of path: \"%s\"" % path)
        if maxpathlength < len(path):
            raise FuseOsError(ENOENT)
        if maxpathlength - 17 < len(path):
            return ['.','..']
        if maxpathlength - 20 < len(path):
            return ['.','..','script.py']
        return folders

if __name__ == '__main__':
    if len(argv) != 2:
        print('usage: %s <mountpoint>' % argv[0])
        exit(1)

    fuse = FUSE(InfinityFS(argv[1],argv[0]), argv[1], foreground=True, allow_other=True)

