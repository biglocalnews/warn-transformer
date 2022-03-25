# Contributing

Clone the repository to your computer and navigate into the directory in your terminal.

The `pipenv` package manager can install all of the Python tools necessary to run and test our code.

```bash
pipenv install --dev
```

Now install `pre-commit` to run a battery of automatic quick fixes against your work.

```bash
pipenv run pre-commit install
```

Create a `.env` file and define your `BLN_API_TOKEN`.

```bash
BLN_API_TOKEN=<yourtoken>
```

Download the raw source files from biglocalnews.org.

```bash
make download
```

Consolidate the raw files into a single file.

```bash
make consolidate
```

Integrate the consolidated file with our latest polished dataset.

```bash
make integrate
```
