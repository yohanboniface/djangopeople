import os
import hashlib

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files import locks
from django.utils.encoding import force_unicode


class HashFileSystemStorage(FileSystemStorage):
    """
    A storage class, using a sha1 hash of the file content as filename;
    if a file with the same hash (content) already exists, it is not
    overwritten.
    Files are written to the local filesystem
    """

    def save(self, name, content):
        dir_name, file_name = os.path.split(name)
        file_root, file_ext = os.path.splitext(file_name)

        file_name = hashlib.sha1(content.read()).hexdigest() + file_ext

        name = os.path.join(dir_name, file_name)
        name = self._save(name, content)

        return force_unicode(name.replace('\\', '/'))

    def _save(self, name, content):
        full_path = self.path(name)
        if not os.path.exists(full_path):
            fd = os.open(full_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_BINARY', 0))
            try:
                locks.lock(fd, locks.LOCK_EX)
                for chunk in content.chunks():
                    os.write(fd, chunk)
            finally:
                locks.unlock(fd)
                os.close(fd)

        if settings.FILE_UPLOAD_PERMISSIONS is not None:
            os.chmod(full_path, settings.FILE_UPLOAD_PERMISSIONS)

        return name
