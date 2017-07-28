
import argparse
import base64
import pyqrcode
import logging
import os
import zbarlight
import hashlib

from pypaperbak.exporters import *
from pypaperbak.importers import *


class PyPaperbakApp:

    """Main app class for the PyPaperBak project."""

    def __init__(self):
        self.logger = logging.getLogger("pypaperback." + self.__class__.__name__)        

    def app_arguments(self):
        """Returns the argparse instance with a description 
        of the apps arguments."""
        parser = argparse.ArgumentParser(                
                description='Backup and restore from paper-backed datastore')
        parser.add_argument('action', choices=['backup', 'restore'], 
                            help='Action to perform ("backup" or "restore")',
                            metavar='ACTION')
        parser.add_argument('infile', 
                            help='Input file or dir',
                            nargs='?',
                            metavar='INFILE')
        parser.add_argument('outfile', 
                            help='Output file/directory',
                            nargs='?',
                            metavar='OUTFILE') 
        parser.add_argument('--exporter', 
                            choices=['pngdir', 'pngzip'],
                            default='pngdir',
                            help='Exporter type. Options: {%(choices)s}. Default: %(default)s',
                            metavar='EXPORTER')      
        parser.add_argument('--baseoutfname', 
                            default='qr-%(qr_number)04d.png',
                            help='Base output filename when using a multi-file exporter. Default: "%(default)s"',
                            metavar='BASEOUTFNAME')              
        parser.add_argument('--pngscale', 
                            type=int,
                            default=2,
                            help='Scale for png output. Default: %(default)s',
                            metavar='SCALE')      
        parser.add_argument('--chunksize', 
                            type=int,
                            default=256,
                            help='How many bytes from the input to read when building a single QR code. Default: %(default)s',
                            metavar='CHUNKSIZE',
                            required=False)      
        parser.add_argument('--fnamepattern', 
                            default='qr-*.png',
                            required=False,
                            metavar='PATTERN',
                            help='Pattern of filenames to look for when importing from a dir. Default: %(default)s')
        parser.add_argument('--sha256',                                                         
                            action='store_true',
                            help='On backup, print the sha256 of the input file. On restore, print the sha256 of the restored file.')
        parser.add_argument('-v', '--verbose', 
                            action='store_true',
                            help='Generate verbose diagnostic to stderr')      
        
                            
        return parser

       
    def main(self, argv):        
        """Entrypoint for the application."""
        arg_parser = self.app_arguments()
        args = arg_parser.parse_args(argv[1:])    
        self.run(args)

    def run(self, args):
        """Run the app given the decoded command line parameters."""        
        if args.verbose:
            logging.basicConfig(format="%(message)s", level=logging.INFO)            
        else:
            logging.basicConfig(format="%(message)s")                

        if args.action == 'backup':
            self.run_backup(args)
        elif args.action == 'restore':
            self.run_restore(args)
        else:
            raise Exception("Unimplemented action: %s" % args.action)

    def run_backup(self, args):
        """Run the backup operation."""                
        
        chunksize = args.chunksize
        encodefunc = base64.b85encode #FIXME: add arg        
        
        infile = open(args.infile, "rb")
        outfile = args.outfile        
        infile_size = os.path.getsize(infile.name)
        hashfunc = hashlib.sha256() if args.sha256 else None

        totalqr = infile_size / chunksize + 1
        self.logger.info('Original file size: %dKiB', infile_size / 1024)
        self.logger.info('Total number of QR codes: %d', totalqr)        

        exporter = self.setup_exporter(args)

        qrnumber = 0
        while True:
            bindata = infile.read(chunksize)
            if not bindata: break
            if hashfunc is not None: hashfunc.update(bindata)

            qrnumber += 1
            self.logger.info('Exporting QR %d of %d', qrnumber, totalqr)
            
            encdata = encodefunc(bindata).decode()            
            qr = pyqrcode.create(encdata)
            exporter.add_qr(qr)
                    
        exporter.finish()
        self.logger.info('Finished exporting')
        if hashfunc is not None: 
            print('SHA-256 of input: %s' % hashfunc.hexdigest())

    def run_restore(self, args): 
        """Run the restore operation."""

        hashfunc = hashlib.sha256() if args.sha256 else None

        if os.path.isdir(args.infile):
            self.logger.info('Setting up PngDirImporter')
            importer = PngDirImporter(args.infile, 
                                      args.fnamepattern)
        else:
            raise Exception('Could not detect import type of file %s' % args.infile)

        decodefunc = base64.b85decode #FIXME: add arg        
    
        with open(args.outfile, "wb") as outfile:
            for image in importer:
                encdata = zbarlight.scan_codes('qrcode', image)                
                bindata = decodefunc(encdata[0])
                outfile.write(bindata)
                if hashfunc is not None: hashfunc.update(bindata)


        self.logger.info('Finished importing')
        if hashfunc is not None: 
            print('SHA-256 of output: %s' % hashfunc.hexdigest())
        

    def setup_exporter(self, args):
        """Setup the exporter according to the specified args."""
        if args.exporter == 'pngdir':
            self.logger.info('Setting up PngDirExporter')
            exp = PngDirExporter(args.outfile, args.baseoutfname,
                                 args.pngscale)
        else:
            raise Exception("Unimplemented exporter type: %s" % args.exporter)

        return exp