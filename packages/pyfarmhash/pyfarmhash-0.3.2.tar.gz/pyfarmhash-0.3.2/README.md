# python-farmhash
Google's FarmHash binding for Python


## Overview

This package provides bindings for the [Google's FarmHash](http://code.google.com/p/farmhash/).  
Code specific to this project is covered by [The MIT License](http://opensource.org/licenses/MIT)

## Install

*Update:* Windows binary wheel uploaded to pypi

Currently, clone the repo and:

pip(Linux & Windows):
```bash
$ sudo pip install pyfarmhash  
```

From Source:
```bash
$ cd python-farmhash  
$ sudo python setup.py Install 
```

### Build on Windows:

1. Install Microsoft Visual C++ Compiler
2. Install miniconda for Python

```bash
$ cd python-farmhash
$ sudo python setup.py install
```

## Usage


```
import farmhash  
print farmhash.hash64('abc')  
2640714258260161385  

For more details, use ipython:
In [1]: import farmhash 

In [2]: farmhash.hash64withseed?  
Type:       builtin_function_or_method  
String Form:<built-in function hash64withseed>  
Docstring:  
Hash function for a string.  For convenience, a 64-bit seed is also hashed into the result.  
example: print farmhash.hash64withseed('abc', 12345)  
13914286602242141520L  
```
