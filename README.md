# BahnBusiness

A library to collect ticket PDFs from bahn.business for bookkeeping purposes.

## Configuration

Provide your bahn.business credentials in a file called `.bahnbusiness-login`.
It may be located either in the current working directory or in your home
directory.

```ini
[bahnbusiness]
username=someuser
password=fancypw
```

## Usage

The main idea behind this module is to be used as a library, it can also be
invoked directly:

```
$ pip install bahnbusiness
$ python -m bahnbusiness
(...)
```

## Development

### Setup

```
$ virtualenv venv --python python3.6
$ source venv/bin/activate
$ pip install -r requirements-dev.txt
$ python setup.py develop
```

### Tests

Since this library is highly dependant on the bahn website and provides very
little functionality on its own, the provided tests are quite minimal. Also,
a valid login is needed to execute them. 

### Publishing

Assuming you have been handed the required credentials, a new version
can be released as follows.

1. adapt the version in `setup.py`, according to [semver](http://semver.org/)
2. commit this change as `Version 1.2.3`
3. tag the resulting commit as `v1.2.3`
4. push the new tag as well as the `master` branch
5. update the package on PyPI:

```
rm dist/*
python setup.py sdist
twine upload dist/*
```
