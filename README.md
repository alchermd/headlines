# Headlines

A Flask powered news aggregation web app.

## Preview

You can view and use the app [here](http://alcherbot.pythonanywhere.com/)

## Installation

0. Make sure you have `python3.6` installed. I suggest you use a virtual environment.

1. Clone the repository.

```bash
$ git clone https://github.com/alchermd/headlines.git
$ cd headlines
```

2. Set the configuration file.

    1. Create an `instance` folder `mkdir instance`
    2. Create a config file `touch instance/appconfig.py`
    3. You need to provide the `appconfig.py` file with the following variables:

    ```py
    # API key from https://newsapi.org
    NEWS_API_KEY = "yourapikey"

    # API key from https://openweathermap.org/api
    WEATHER_API_KEY = "yourapikey"

    # API key from https://openexchangerates.org/
    RATES_API_KEY = "yourapikey"

    # Secret key used by the Flask app.
    SECRET_KEY = "really hard to guess string"
    ```

3. Install the app as a package.

    1. Install dependencies `pip install -r requirements.txt`

    2. Install the app `pip install -e .`

    3. Set the Flask environment variables.

    ```bash
    $ export FLASK_APP=headlines
    $ export FLASK_DEBUG=1
    ```

    4. Run the app with `flask run`.

    5. Visit `localhost:5000/` and enjoy!

## Contributing

I'm happy to hear your thoughts! I'd appreciate you openin an issue or a creating a pull request :smiley:

## License

See [LICENSE](/LICENSE) for more information.