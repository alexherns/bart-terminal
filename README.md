# bart-terminal

## Usage
```bash
$ python app.py

<Train: FRMT>
<Estimate: 5 cars in 6 minutes
<Estimate: 6 cars in 21 minutes
<Estimate: 6 cars in 36 minutes
<Train: MLBR>
<Estimate: 9 cars in 13 minutes
<Estimate: 9 cars in 28 minutes
<Estimate: 9 cars in 43 minutes
```

## Installation
See requirements.txt for necessary Python 2.7 packages to install. You can use pip to install the packages:
```bash
$ pip install -r requirements.txt
```

A default API key is included in the script, but I don't know if they will limit your usage if you request too often. It's easy to request a key from http://api.bart.gov/api/register.aspx. After that, you can set an environment variable to the BART key (BART\_API\_KEY). For example (using the default key):
```bash
$ export BART_API_KEY="MW9S-E7SL-26DU-VV8V"
```

## Coming soon
- setup.py for easy installation
- command-line flags to query your origin and direction
- configurations to set a default origin and direction (e.g. "home" or "work" origins)
- A curses UI?
