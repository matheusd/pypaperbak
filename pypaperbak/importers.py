
import os
import glob
import logging
from PIL import Image
import zbarlight

class PngDirImporter:
    """Importer for the pngdir exporter. Works as an iterator, returning 
    the next PNG image for decoding."""

    def __init__(self, basedir, fname_pattern):
        self.basedir = basedir        
        self.fname_pattern = fname_pattern
        self.logger = logging.getLogger("pypaperbak." + self.__class__.__name__)

        glob_pattern = os.path.join(self.basedir, self.fname_pattern)
        self.logger.info("Looking for files as %s", glob_pattern)
        self.files = sorted(glob.glob(glob_pattern))
        self.file_idx = 0

    def __iter__(self):
        return self

    def __next__(self):
        """Import the next block of data (next png file)"""
        if self.file_idx >= len(self.files):
            raise StopIteration()

        fname = os.path.realpath(self.files[self.file_idx])
        self.logger.info("Importing %s", fname)
        self.file_idx += 1
        with open(fname, 'rb') as image_file:
            image = Image.open(image_file)
            image.load()
            return image        


    