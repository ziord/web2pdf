from web2pdf.pkg import get_info
data = get_info()
__version__ = data["version"]
__author__ = data["author"]
