
import os

class PyPaperExporterException(Exception):
    pass

class PngDirExporter():
    """Exports the data as a series of png files in a given dir."""

    def __init__(self, destdir, basefname, scale=1):    
        """Initialize the png dir exporter. """
        self.destdir = destdir
        self.basefname = basefname
        self.qr_number = 0
        self.scale = scale

        if not os.path.exists(self.destdir):
            os.makedirs(self.destdir)
        if not os.path.isdir(self.destdir):
            raise PyPaperExporterException("Cannot use PngDirExporter to export to non-dir: %s" % self.destdir)

    def add_qr(self, qr):
        """Add the qr to the export."""
        self.qr_number += 1

        fname_pmts = {
            'qr_number': self.qr_number
        }

        fname = self.basefname % fname_pmts
        fullfname = os.path.join(self.destdir, fname)
        qr.png(fullfname, scale=self.scale)        


    def finish(self):
        """Finish exporting all qr codes. This exporter does nothing
        extra."""
        pass
