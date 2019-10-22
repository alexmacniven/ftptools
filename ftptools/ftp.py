from ftplib import FTP

from .connection import Connection


class FTPConnection(Connection):
    def refresh(self):
        self.logger.info("(re)establishing connection")
        self.conn = FTP(host=self.host, user=self.user, passwd=self.pasw)
