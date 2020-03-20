# web2pdf

A "pluggable" utitility tool for converting web pages to pdf files, written in Python

## Usage

You have to define a function that takes in two arguments and returns two a tuple of two lists:

```python
def spawn_urls(site_url: str, base_url: str) -> Tuple[List[str], List[str]]:
    #your code goes here
    ...
```
```site_url``` is the link to the page you want to convert
```base_url``` is the base name you would like to call that link
For example: 
if you want to save a page: ```myexample.testing.com\apage```, then ```site_url``` would be ```myexample.testing.com\apage```, and ```base_url``` could be ```myexample.testing.com``` or whatever you choose.
The most important point to note is that, your function ```spawn_urls()``` (could be named something different) returns two ```list```s, the first containing all the links to the pages you would like to save, and the second containing the titles you'd use to refer to those links. The links and titles ```list```s must correspond if you want a pdf with an ordered title.

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

#import the w2pconverter
from web2pdf.core import w2pconverter

#define your url/title generating function
def spawn_urls(site_url, base_url):
    ...

site_url, base_url = 'myexample.testing.com\apage', 'myexample'

#call web2pdf()
w2pconverter.web2pdf('mypdf.pdf', spawn_urls, **dict(site_url=site_url, base_url=base_url))

#alternatively
args_dict = {'site_url' : site_url, 'base_url': base_url}  #use keys that corresponds to your function's arguments
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


