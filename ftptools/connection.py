import logging

from os import listdir
from pathlib import Path
from shutil import move
from tempfile import TemporaryDirectory


class Connection:
    def __init__(self, host, user, pasw):
        self.logger = logging.getLogger(__name__)
        self.host = host
        self.user = user
        self.pasw = pasw
        self.conn = None
        self.refresh()

        self.store = TemporaryDirectory()
        self.logger.info(f"store @ {self.store.name}")

    def __del__(self):
        self.conn.close()
        self.store.cleanup()

    def refresh(self):
        raise NotImplementedError

    def fetch_modtime(self, filename):
        """Returns last write time of filename.
        Args:
            filename: string: file name
        Returns:
            int: last write time of file
        Raises:
            FileNotFoundError
        """
        filelist = self.conn.mlsd()
        for fi in filelist:
            if filename in fi[0]:
                modtime = int(fi[1]["modify"])
                self.logger.info(f"mod time for {filename} @ {modtime}")
                return modtime
        return FileNotFoundError

    def fetch_files(self, files=None):
        """Downloads files to instances storage directory.
        Args:
            files: list[str]: list of files to download.
        Returns:
            list[str]: list of files failed to download.
        Note:
            When no files argument supplied; all files in
            the present workin directory will be downloaded.
        """
        fails = list()
        if (files is None) or (files[0] is None):
            files = self.conn.nlst()
        for fileitem in files:
            try:
                with open(Path(self.store.name, fileitem), "wb") as fileobj:
                    self.logger.info(f"retrieving {fileitem}")
                    self.conn.retrbinary(f"RETR {fileitem}", fileobj.write)
            except OSError:
                self.logger.warning(f"{fileitem} has failed")
                fails.append(fileitem)
        return fails

    def move_generator(self, destination_dir):
        """Moves contents of instance store to a destination.
        Args:
            destination_dir: str: path to destination directory
        Yields:
            str: file name moved
        Raises:
            StopIteration
        """
        directory_list = listdir(self.store.name)
        for file in directory_list:
            source = Path(self.store.name, file)
            destination = Path(destination_dir, file)
            self.logger.info(f"move item {source} to {destination}")
            move(source, destination)
            yield file
