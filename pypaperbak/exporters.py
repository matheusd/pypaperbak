
import os
from fpdf import FPDF
import tempfile

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


    def finish(self, inputhash):
        """Finish exporting all qr codes. This exporter does nothing
        extra."""
        pass


class PDFExporter():
    """Exports the set of QR codes as a PDF file."""
    def __init__(self, fname):
        self.pdf = FPDF()
        self.fname = fname
        self.qrnumber = 0

        self.pdf.set_font('Arial', '', 10)
        self.pdf.set_creator('PyPaperBak - https://github.com/matheusd/pypaperbak')
        self.pdf.set_title('PyPaperBak Document')

        self.tmpfilenames = dict()

        # TODO: Parametrize this
        self.format = 'A4'
        page_width = 210
        page_height = 297
        self.qr_margin = 5
        self.qr_per_row = 3
        self.qr_rows_per_page = 5
        self.qr_per_page = self.qr_per_row * self.qr_rows_per_page

        # to discover the size, calculate the minimum size to fit as
        # many requested QR's per row and page, giving a 
        # margin at each end and between the codes
        self.qr_size = min( (page_width - self.qr_per_row*self.qr_margin - self.qr_margin) / self.qr_per_row,
                            (page_height - self.qr_rows_per_page*self.qr_margin - self.qr_margin) / self.qr_rows_per_page  )        
                       
        self.qr_margin_x = (page_width - self.qr_size*self.qr_per_row) / (self.qr_per_row+1)
        self.qr_margin_y = (page_height - self.qr_size*self.qr_rows_per_page) / (self.qr_rows_per_page+1)

    def add_qr(self, qr):        
        if (self.qrnumber % self.qr_per_page) == 0:            
            self.pdf.add_page()

        while True:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as file:
                tmpname = file.name         
            # make sure we don't get a repeat tmpname because fpdf will only
            # include one copy of a given filename
            if not tmpname in self.tmpfilenames: break
        self.tmpfilenames[tmpname] = True
        qr.png(tmpname, scale=6)
        
        idxinpage = self.qrnumber % self.qr_per_page
        col = idxinpage % self.qr_per_row
        row = int(idxinpage / self.qr_per_row) 
        size = self.qr_size
        margin_x = self.qr_margin_x
        margin_y = self.qr_margin_y

        self.pdf.image(
                tmpname, 
                margin_x + col * (size + margin_x),  # X 
                margin_y + row * (size + margin_y),  # Y
                size,                                # width    
                size)                                # height
        os.unlink(tmpname)        

        self.qrnumber += 1
    

    def finish(self, inputhash):
        """Finish exporting the pdf."""
        self.pdf.set_xy(self.qr_margin_x, -22)        
        self.pdf.write(0, 'Hash of original document: %s' % inputhash.hexdigest())
        self.pdf.output(self.fname)
