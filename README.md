# web2pdf

A "pluggable" utitility tool for converting web pages to pdf files, written in Python

## Usage

You have to define a function that generates the web page(s) URL(s) with corresponding title(s), and returns the URL(s) and title(s) as a tuple of two lists:

```python
def spawn_urls(...) -> Tuple[List[str], List[str]]:
    # your code goes here
    ...
```

In otherwords, your function ```spawn_urls()``` (could be named something different) returns two ```list```s, the first containing all the links to the pages you would like to save, and the second containing the titles you'd use to refer to those links. The links and titles ```list```s must correspond if you want a pdf with an ordered title.

### Note
The links and titles lists should be ordered/sorted in the way you want the pages to appear (if converting multiple webpages at once), but if it isn't web2pdf would sort the list using regular string sorting, which might not be what you want.
Example: 
```python
_list_of_links = [
    'mylink.com',
    'mylink2.com',
    'mylink3.com'
]
_list_of_titles = [
    '01#title',
    '02#title',
    '03#title'
]
```
In this example ```_list_of_links``` and ```_list_of_titles``` _corresponds_ or are ordered, and when the pdf is generated, the first page would be ```'mylink.com'``` which corresponds to the title ```'01#title'```

```python

# import the w2pconverter
from web2pdf.core import w2pconverter

# define your url/title generating function
def spawn_urls(...) -> Tuple[List[str], List[str]]:
    ...

# Again, spawn_urls must return a tuple of lists -> Tuple[List[str], List[str]]
# the first element list must contain the URLs, and the second element list must contain your choice of "title" for each corresponding URL in the first element list.

# call web2pdf()
w2pconverter.web2pdf('mypdf.pdf', spawn_urls, **dict(your_arg=your_arg_value, ...))

# alternatively
args_dict = {'your_arg' : your_arg_value, ...}  # use keys that corresponds to your function's arguments
w2pconverter.web2pdf('mypdf.pdf', spawn_urls, **args_dict)

```
This would generate the pdf in a  ```converted``` folder in your current working directory.

## Dependencies

You must have the following:
* [chrome webdriver](https://chromedriver.chromium.org/downloads) installed and set to path. Chrome browser version must match Chrome driver version.
* Python >= 3.5


## Supported Platforms

```Web2pdf``` currently supports only Linux and Windows platforms


## Installation

Clone this repo and do:
```
cd web2pdf
python setup.py install
```


