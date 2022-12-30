# Forum123 backend

## Development setup

__This project requires Python 3.10.__



### First time setup

If this is your first run of this project you need to create and activate python virtual environment.
You can do it in the way you are more familiar with but here is an example of how it can be done:

1. Go to the project root directory.
2. Create virtual environment: `python3.10 -m venv .venv/forum123`
3. Activate virtual environment: `source .venv/forum123/bin/activate`
4. Install dependencies: `pip install -r requirements.txt -r requirements-dev.txt`

_Note_: If you've created a virtual environment inside project directory
and don't want it to be tracked by git, please do not add it to `.gitignore` file.
There are other ways to do it correctly - choose any of these or find your own:

- Add virtual environment directory to `.git/info/exclude` file of this repository.
- Add local `.gitignore` file to the directory of your virtual env and put `*` inside this file.



### Run linters

1. Go to the project root directory.
2. Activate python virtual environment.
3. Run `mypy`
4. Run `flake8`
5. Run `pylint src`

Linters order above is the preffered way to run and fix them one by one.



### Run application

1. Open terminal.
2. Depnding on your OS, type in a command 'export FLASK_APP=src' for Linux
    or 'set ...' for Windows.
3. Type 'flask run' command in terminal.
4. Open http://127.0.0.1:5000 in your internet browser.
