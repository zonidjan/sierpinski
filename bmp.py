# bmp - bitmap processing
# ref: https://en.wikipedia.org/wiki/BMP_file_format

from struct import unpack

class FormatError(Exception): pass
class MagicError(FileFormatError): pass
class CompressionError(FormatError): pass
class BppError(FormatError): pass

class Bmp(object):
	def __init__(self, fn_or_fo):
		fo = fn_or_fo
		if isinstance(fn_or_fo, basestring):
			fo = open(fn, 'rb')
		self.fo = fo
		self._read()
	def _read(self):
		header = self.fo.read(14)
		magic, filesize, start_address = unpack("<2sI2x2xI", header)
		if magic != "BM": raise MagicError("wrong BMP header magic")
		dib = self.fo.read(40)
		magic, pixelwidth, pixelheight, bpp, compression = unpack("<III2xHI4x4x4x4x4x", dib)
		if magic != 40: raise MagicError("wrong DIB header magic")
		if compression != 0: raise CompressionError("compression not supported")
