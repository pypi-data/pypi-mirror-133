# drinkingbird

Program to keep your browser/computer active.

![Alt Text](img/drinkingbird.gif)

## Installation

Assuming you have a [Python3](https://www.python.org/) distribution
with [pip](https://pip.pypa.io/en/stable/installing/), to install a development version, cd to the directory with this
file and:

```
pip3 install -e .
```

As an alternative, a virtualenv might be used to install the package:

```
# Prepare a clean virtualenv and activate it
virtualenv -p /usr/bin/python3.6 venv
source venv/bin/activate
# Install the package
pip3 install -e .
```

To install also the dependencies to run the tests or to generate the documentation install some of the extras like

```
pip3 install -e '.[docs,test]'
```

Mind the quotes.

## Usage

To run, open a browser in the foreground and execute:

```
drinkingbird
```

This will cycle tabs each 10 s.

To stop it, just press Esc.

For more options see

```
drinkingbird --help
```
