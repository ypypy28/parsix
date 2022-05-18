# Parsix - парсер избирательных комиссий.

A simple parser of Russian election commissions from the official website. Use it to get names of members and location of the election commissions in the chosen region of Russia.

To start using this parser You will have to install [chrome webdriver](https://chromedriver.chromium.org) if you don't already have it.

Example usage:

```sh
python3 parsix --region=ivanovo
```


By default, you will get the data in two separate CSV files inside the folder named _out_ in your current directory. You can pass a _--output-dir_ argument with the path to a specific directory. Each file will have current date as a part of the name, one file if for the data of precinct election commissions and another is for higher election commissions. You will be able to pass these CSV-files in the Google Maps.
