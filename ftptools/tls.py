from ftplib import FTP_TLS

from .connection import Connection


class TLSConnection(Connection):
    def refresh(self):
        self.logger.info("(re)establishing connection")
        self.conn = FTP_TLS(self.host)
        self.conn.login(self.user, self.pasw)
        self.conn.prot_p()
