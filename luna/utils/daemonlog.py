#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
Read a compact exception from the local daemon log after an HTTP 500.
Existing logs have no request ID, so matching by time, path and method is best
effort. Never select an old entry or guess between multiple matching entries.
"""

import os
import re
import socket
import stat
from configparser import RawConfigParser
from typing import BinaryIO
from urllib.parse import urlsplit

from requests import Response
from requests.utils import get_environ_proxies

from luna.utils.constant import DAEMON_INI_FILE, DAEMON_LOG_FILE

Snapshot = tuple[str, int, int, int, bytes, str, str]


class DaemonLog:
    """
    Bounded, optional log lookup; failures leave the original HTTP error intact.
    """

    LIMIT = 128 * 1024
    RECORD = re.compile(r'^\[(?:DEBUG|INFO|WARNING|ERROR|CRITICAL)\]:', re.MULTILINE)
    FRAME = re.compile(r'^  File "([^"\n]+)", line (\d+)(?:, in ([^\n]+))?$', re.MULTILINE)
    EXCEPTION = re.compile(r'^[^\W\d]\w*(?:\.[^\W\d]\w*)*(?::[^\n]*)?$', re.MULTILINE)

    @staticmethod
    def local_url(url: str) -> bool:
        """
        Only a direct endpoint whose resolved addresses belong to this machine.
        Binding an ephemeral socket checks local addresses without connecting.
        """
        parsed = urlsplit(url)
        if parsed.scheme not in ('http', 'https') or not parsed.hostname or get_environ_proxies(url):
            return False
        addresses = socket.getaddrinfo(parsed.hostname, 0, type=socket.SOCK_STREAM)
        if not addresses:
            return False
        for family, kind, protocol, _, address in addresses:
            with socket.socket(family, kind, protocol) as probe:
                probe.bind(address)
        return True

    @staticmethod
    def logfile() -> str:
        """
        Use the daemon's configured file, or the TrinityX default if unreadable.
        The CLI's own LOGGER section describes a different log.
        """
        parser = RawConfigParser()
        try:
            parser.read(DAEMON_INI_FILE)
            return parser.get('LOGGER', 'LOGFILE', fallback=DAEMON_LOG_FILE)
        except Exception:
            return DAEMON_LOG_FILE

    @staticmethod
    def open_log(path: str) -> BinaryIO:
        """
        Reject devices and pipes without waiting for a writer.
        """
        descriptor = os.open(path, os.O_RDONLY | getattr(os, 'O_NONBLOCK', 0))
        try:
            if not stat.S_ISREG(os.fstat(descriptor).st_mode):
                raise OSError('The daemon log is not a regular file')
            return os.fdopen(descriptor, 'rb')
        except Exception:
            os.close(descriptor)
            raise

    @classmethod
    def capture(cls, url: str, method: str) -> Snapshot | None:
        """
        Save the log position immediately before each physical HTTP request.
        A short anchor also detects truncation followed by rapid log growth.
        """
        try:
            if not cls.local_url(url):
                return None
            path = cls.logfile()
            with cls.open_log(path) as logfile:
                info = os.fstat(logfile.fileno())
                logfile.seek(max(0, info.st_size - 256))
                anchor = logfile.read(256)
            return (path, info.st_dev, info.st_ino, info.st_size, anchor, url, method.upper())
        except Exception:
            return None

    @classmethod
    def detail(cls, snapshot: Snapshot | None, response: Response) -> str | None:
        """
        Read only new bytes from the same file and reject redirects or ambiguity.
        Rotation, permissions, malformed or oversized logs are normal fallbacks.
        """
        try:
            if snapshot is None or response.history:
                return None
            path, device, inode, offset, anchor, url, method = snapshot
            if urlsplit(response.url)._replace(query='', fragment='') != urlsplit(url)._replace(query='', fragment=''):
                return None
            with cls.open_log(path) as logfile:
                info = os.fstat(logfile.fileno())
                if (info.st_dev, info.st_ino) != (device, inode) or not offset <= info.st_size <= offset + cls.LIMIT:
                    return None
                logfile.seek(max(0, offset - 256))
                if logfile.read(len(anchor)) != anchor:
                    return None
                logfile.seek(offset)
                content = logfile.read(info.st_size - offset).decode('utf-8', errors='replace')
            return cls.parse(content, urlsplit(url).path or '/', method)
        except Exception:
            return None

    @staticmethod
    def clean(value: str) -> str:
        """
        Bound display text and strip controls before writing it to a terminal.
        """
        return ' '.join(''.join(char if char.isprintable() else ' ' for char in value).split())[:1000]

    @classmethod
    def exception_record(cls, content: str, path: str, method: str) -> str | None:
        """
        Select one complete Flask exception record for this path and method.
        """
        if not content.endswith('\n') or not cls.RECORD.match(content):
            return None
        starts = [match.start() for match in cls.RECORD.finditer(content)] + [len(content)]
        records = [content[start:end] for start, end in zip(starts, starts[1:])]
        header = f' - Exception on {path} [{method}]'
        matches = [record for record in records if record.startswith('[ERROR]:')
                   and re.search(r'\[app\.py:log_exception@\d+\]', record.split('\n', 1)[0])
                   and record.split('\n', 1)[0].endswith(header)]
        if len(matches) != 1:
            return None
        return matches[0]

    @classmethod
    def parse(cls, content: str, path: str, method: str) -> str | None:
        """
        Show the innermost location and exception only, never source or payloads.
        """
        record = cls.exception_record(content, path, method)
        if record is None or '\nTraceback (most recent call last):\n' not in record:
            return None
        frames = list(cls.FRAME.finditer(record))
        if not frames:
            return None
        # Unrecognized multiline endings or interleaved records are not a usable trace.
        exceptions = [exception for exception in cls.EXCEPTION.finditer(record)
                      if exception.start() > frames[-1].end()]
        if len(exceptions) != 1 or record[exceptions[-1].end():].strip():
            return None
        filename, line, function = frames[-1].groups()
        filename = filename.replace('\\', '/')
        filename = filename.rsplit('/daemon/', 1)[-1] if '/daemon/' in filename else filename.rsplit('/', 1)[-1]
        if '..' in filename.split('/'):
            return None
        reason = exceptions[-1].group()
        location = f'{cls.clean(filename)}:{cls.clean(line)}'
        if function:
            location += f', in {cls.clean(function)}'
        return f'{cls.clean(reason)} ({location})'
