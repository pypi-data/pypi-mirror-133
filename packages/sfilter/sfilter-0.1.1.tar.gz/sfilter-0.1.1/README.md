# sfilter (Pre-Alpha)

Tool for filtering out stinky/smelling code

## Usage

```shell
pip install sfilter
sfilter <path to project or file>
```

## Install and test the project

### Precondition

1. [make](https://www.gnu.org/software/make/) is installed
2. [pipenv](https://pipenv.pypa.io/en/latest/#install-pipenv-today) is installed
3. [pyenv](https://github.com/pyenv/pyenv#installation) 
   is installed with the following python versions:
     - 3.7.12
     - 3.8.12
     - 3.9.1 
4. Run make command:
   ```shell
   make install
   ```

### Test project

Test the project after each code change by running make:
```shell
make test
```

## Publish

### Test locally

```shell
pip install -e .
```

### Prepare to publish the project

```shell
PIPENV_IGNORE_VIRTUALENVS=1 pipenv run python setup.py bdist_wheel
PIPENV_IGNORE_VIRTUALENVS=1 pipenv run pip install -e .
pipenv shell
sfilter src/sfilter
exit
PIPENV_IGNORE_VIRTUALENVS=1 pipenv run python setup.py sdist
tar tzf dist/sfilter-<version>.tar.gz 
```

### Upload to pypi

```shell
twine upload dist/*
```
