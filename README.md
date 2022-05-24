# Parsix – парсер избирательных комиссий

A simple parser of Russian election commissions from the official website. Use it to get names of members and locations of the election commissions in the chosen region of Russia.

To start using this parser you have to install [chrome webdriver](https://chromedriver.chromium.org) if you don't already have it.

## Usage 

Simple usage:

```sh
parsix --region=ivanovo
```


By default, you will get the data in two separate CSV files inside the directory named `out` in your current directory. You can pass an `--output-dir` argument with the path to a specific directory for the output files. Each file will have current date as a part of the name, one file is for the data of precinct election commissions and another is for higher election commissions. You will be able to upload these CSV-files in the Google Maps.


## Installation
To use it as a cli tool run this commands
```sh
git clone https://github.com/ypypy28/parsix.git
cd parsix
pip install . --user

```


## Installation for development

1. Install [chrome webdriver](https://chromedriver.chromium.org) (and Chrome or Chromium web browser if you don't already have it)
2. Clone this project into your local directory of choice

```sh
git clone https://github.com/ypypy28/parsix.git
cd parsix
```
3. Install dependencies in virtual environment
- with [pipenv](https://pipenv.pypa.io/en/latest/)

```sh
pipenv sync --dev
```
- or with out of box `pip` on \*nix-systems
```sh
python3 -m venv venv
source ./venv/bin/activate
pip install -e .
```
- or with `pip` in powershell on windows
```powershell
python -m venv venv
.\venv\Scripts\activate.ps1
pip install -e .
```

4. Now you should be able to run `parsix` as a module from your virtual environment
```sh
python3 -m parsix --region=ivanovo
```

or like a regular cli application because of the installation in editable mode
```sh
parsix --region=ivanovo
```

## Build 
If you want to build a package, you can do it with a simple command
```sh
pipenv run build
```
