
# PyPaperBak

Backup and restore binary data from paper-backed datastore.

PyPaperBak reads data from any file (including binary files), generates QR Codes from successive chunks of the file and writes it to a series of png or a single pdf file.

The restore operation works in reverse: reads the QR codes from a single or a series of images and restores the original file.

## Use Cases

  - Backing up any file you want to restore later, without needing to use OCR
  - Backing up [KeePassX](https://www.keepassx.org/) files
  - Backing up seed files from crypto wallets

## Storage Capacity

Storage capacity for a single A4 leaf is 15 QR Codes, each storing 256 bits of the original file, for a grand total of *3840 bytes per page*.

In the current version (v1.0.0) these values are hard coded but on a future version they may be modifiable by command line arguments.

## Installation

Download and extract one of the releases or download the python source code and execute.


## Basic Usage

Using `--sha256` prints the hash of the input (on backup) or output (on restore) file.

```shell
  $ pypaperbak --sha256 --exporter pdf backup samples/medium.txt output.pdf
  $ pypaperbak --sha256 --fnamepattern *.jpg restore scanned-images/ restored.txt
```


## Technical Aspects

The general backup procedure is the following:

  - Grab a chunk of the input file
  - Frame the chunk with a header/footer
  - Encode the binary data using a binary-to-text encoding (base85 in the current version)
  - Generate the QR code from the encoded text
  - Generate the png representation of the QR code


The restore action performs the operations in reverse.



## Examples

Generate a pdf file from medium.txt:

```shell
  $ pypaperbak --sha256 --exporter pdf backup samples/medium.txt output.pdf
  Finished Exporting
  SHA-256 of input: b33d0c46df78715005bcc28db070a63e938b4e3ce4052365fc5714b321f498f3
```

Extract the images from the pdf (requires `pdfimages`/`poppler-utils`) and verify generation:
  
```shell
  $ pdfimages -png output.pdf imgs-pdf/
  
  $ pypaperbak -v --sha256 --fnamepattern *.png restore imgs-pdf/ restored.txt
  Finished importing
  SHA-256 of output: b33d0c46df78715005bcc28db070a63e938b4e3ce4052365fc5714b321f498f3
```

Convert the pdf to one jpg per page and import (requires `convert`/`ghostscript`):

```shell
  $ convert -quality 90 -density 200x200 output.pdf imgs-single/single%d.jpg

  $ pypaperbak -v --sha256 --fnamepattern *.jpg restore imgs-single/ restored.txt
  Finished importing
  SHA-256 of output: b33d0c46df78715005bcc28db070a63e938b4e3ce4052365fc5714b321f498f3
```

Restore from a single png image:

```shell
  $ openssl sha256 samples/small.txt
  SHA256(samples/small.txt)= d51c36f2a07e7311e1d5b79d1dc16f9e5c07b116cb65b42a2b45992ccd0b29ca

  $ pypaperbak -v --sha256  restore samples/damaged-small.png restored.txt
  Finished importing
  SHA-256 of output: d51c36f2a07e7311e1d5b79d1dc16f9e5c07b116cb65b42a2b45992ccd0b29ca
```