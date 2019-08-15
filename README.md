# BaiskoafuDown

[BaiskoafuDown](https://github.com/R00t173/BaiskoafuDown.git) is a simple program to download songs, movies, series from [Baiskoafu](https://baiskoafu.com).
### Installation
Simply clone the repo from git.
```sh
$ git clone https://github.com/R00t173/BaiskoafuDown.git
```
### config.py
Login details are required
```python
username = "your email here"    # email
password = "your password here" # password
media_quality(quality='medium') # set quality['high', 'low', 'medium']
ASK_BEFORE_DOWNLOAD = True      # set 'False' to download without prompt
IS_PRIMARY_DEVICE   = True	    # set 'True' only if you have premium subscription
```
### Usage
This script requires Python 3.6 or later and the python3 requests module to work. To install this module, run this in your terminal: "python3 -m pip install requests"
```sh
$ python3 -m pip install requests
```
### Run program
```sh
$ cd BaiskoafuDown
$ python3 baiskoafuDown.py
```
### with an argument
```sh
$ python3 baiskoafuDown.py "name of a song or movie"
```
