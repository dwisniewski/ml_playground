# ml_playground: Sample ML project configured "right"
This configuration assures less pain in the future

### Step 1: Manage requirements with Poetry (better than virtualenv + pip install)
Context: [Short 3 minutes video intro](https://www.youtube.com/watch?v=V7UhzA4g2yg) [Documentation](https://python-poetry.org/) [Tutorial](https://python-poetry.org/docs/basic-usage/)

Classically, we manually managed all packages that were required by our projects. Using the `pip` tool, for example, we could download and install packages, such as pandas via `pip install pandas` or even restrict an installation providing a specific version, e.g., `pip install pandas==1.5.2`.

However, as APIs of these tools frequently evolve, we had to list all of our libraries along with their versions in a file that any other person could reuse to install the same versions of packages as we used to ensure that the code works fine. We could create a file named `requirements.txt` with a list of all requirements and upload it into `GitHub` so that the installation of all packages would require running only the `pip install -r requirements.txt` command. 

However, managing `requirements.txt` was frequently a manual task forcing us, e.g., to run `pip freeze | TOOLNAME >> requirements.txt` to append the file with an entry consisting of a pair of a TOOLNAME's name and its version that we installed on our computer -- it was easy to forget about it.

Moreover, developing various projects, we could face a situation in which `project A` requires `pandas` in version `1.5.2` and `project B` required it in version `0.9.2`. How to deal with it when by default `python` installs packages globally and allows us to have only one version of a package? We used `virtualenv` to create separate virtual environments for each project. In each virtual environment, one could install all dependencies locally so that `project A` could use different versions than `project B`.
Both `pip` and `virtualenv` requires us to remember multiple steps:

`virtualenv venv` -- to initialize virtualenv named `venv` at the beginning of our work with the project
`source venv/bin/activate` -- to use virtualenv named `venv` every time we start to work on a project
`pip install PACKAGE` -- to install a package 
`pip freeze | grep PACKAGE >> requirements.txt` -- to add the PACKAGE with its version to the `requirements.txt` file
`deactivate` -- to exit virtualenv


To help us, `poetry` was developed. It manages `virtualenv`s and automatically keeps track of the tools we install so that we don't have to enable virtualenvs manually nor remember to update the `requirements.txt` file.

To use `poetry`, we need to install it first: `pip install poetry`, then I would recommend setting `poetry config virtualenvs.in-project true` to force `poetry` to create virtual environments in the project`s folder (otherwise it creates them in a common folder).


1) We may use `poetry new PROJECTNAME` to create a basic project structure:
```bash
poetry-demo
├── pyproject.toml
├── README.md
├── poetry_demo
│   └── __init__.py
└── tests
    └── __init__.py
```

The most important file here is `pyproject.toml`, which is recently suggested as the core settings file used to build packages. You can read more about it in a nice [blogpost](https://betterprogramming.pub/a-pyproject-toml-developers-cheat-sheet-5782801fb3ed) or more in-depth in [PEP 518](https://peps.python.org/pep-0518/). In short, `pyproject.toml` helps us to publish python projects and stores metadata as well as information about dependencies.

 **IMPORTANT!** If you already have a project structure, you can use `poetry init` so that only `pyproject.toml` will be created.
 
2) Enable virtualenv with `poetry env use python3.10` if you have `python3.10` installed on your computer, otherwise, choose your version. Once you do this, you don't have to remember to activate or deactivate virtual environments -- `poetry` will do it for you!

3) Install dependencies, e.g., using `poetry add pandas` or `poetry add pandas@1.5.2` if you need a specific version. Viola! `pandas` is installed and the information about the package is automatically added to `pyproject.toml` and `poetry.lock` ([why?](https://betterdev.blog/pin-exact-dependency-versions/)) so you don't have to update `requirements.txt` manually.

4) If you download a repository and want to install all dependencies use the `poetry install` command in the project folder.



### Step 2: Listing files to ignore
If your project creates some files you don't want to track, create a `.gitignore` file and list the files/folders to ignore (e.g., `*.pyc` to ignore all `pyc` files).

You can read more about `.gitignore` files [here](https://www.atlassian.com/git/tutorials/saving-changes/gitignore)

### Step 3: (DVC) Handling big files (models, datasets)
Context: [Documentation](https://dvc.org/)

Git is not good at handling large files. Especially binary files (e.g., ML models) for which diffs don't make sense. For this reason, we can use `DVC` to store large files outside of git while tracking their versions and changes.

[Detailed instructions](https://dvc.org/doc/start/data-management/data-versioning)

a) Install DVC: `pip install dvc`

b) Init DVC inside your GIT repo: `dvc init`

As a result some files are created. We need to add them to Git:

```bash
git status
Changes to be committed:
        new file:   .dvc/.gitignore
        new file:   .dvc/config
        ...
git commit -m "Initialize DVC"
```
c) Configure your storage:
We need to tell DVC where large files should be physically located. They may be placed in various places such as Amazon S3, Google Drive, regular folders. Let's use some already created folder under `/tmp/storage`

`dvc remote add -d mystorage /tmp/storage` -- create storage `mystorage` in a given place and make it default `-d`.

As a result the `.dvc/config` file is updated so that we need to add it to our repo:

```bash
git add .dvc/config
git commit -m "[DVC] Remote initialization"
```

Now we can manage our data with DVC.

To track a file or directory with DVC use: `dvc add PATH_OR_DIR`, e.g., `dvc add dataset/data.gz`
As a result, DVC creates `*.dvc` file which will be versioned in GIT. However the actual files will be stored in `mystorage` and `*.dvc` file helps us to identify which file from storage we need.

Let's add those metadata to Git: 
```
git add dataset/data.gz.dvc dataset/.gitignore
git commit -m "Add data"
```

Then, even if we delete the actual file, we can use `dvc pull` to download the files from storage or `dvc push` to upload to storage. These files are frequently used with `git pull/push` commands.

### Step 4: (pre-commit) Encorcing coding workflow
Frequently, we forget about assuring good quality of the code we push to repositories. Using pre-commit Git hooks may force to apply some procedures at the moment of creating each commit. To achieve that, a simple approach is to use `pre-commit` framework.

Context: [Documentation](https://pre-commit.com/)

a) Install `pre-commit`: `pip install pre-commit`

b) Create a configuration file `.pre-commit-config.yaml` in the root folder of your repo, which describes the steps to perform before applying each commit. My configuration is:

```yaml
repos:
-   repo: https://github.com/pycqa/isort
    rev: 5.11.2
    hooks:
    - id: isort
      name: isort (python)
-   repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
    -   id: black
        args: [--safe]
-   repo: https://github.com/pycqa/flake8
    rev: 3.7.9
    hooks:
    -    id: flake8
-   repo: https://github.com/pre-commit/mirrors-mypy
    rev: 'v0.991'
    hooks:
    -   id: mypy
        additional_dependencies: [tokenize-rt==3.2.0]
- repo: https://github.com/econchick/interrogate
  rev: 1.5.0  
  hooks:
    - id: interrogate
      args: [--vv, -i, --fail-under=80]
- repo: local
  hooks:
    - id: pytest-check
      name: pytest-check
      stages: [commit]
      types: [python]
      entry: pytest
      language: system
      pass_filenames: false
      always_run: true 
```

This config lists all the tools to use, their repository names and optional parameters. Note: `pre-commit` creates a separate `venv` in which it uses the tools.

c) Install the hooks: `pre-commit install`

d) Check how it works -- after each `git commit`, `pre-commit` runs all the tools listed in the `.pre-commit-config.yaml` and allows to commit if all of them pass. If not, it forces us to fix errors or uses the tools to fix them (depending on tool).

An example output:
```bash
(venv)  git commit -a -m "Initialization"                            Thu 29 Dec 2022 09:45:59 PM CET
[INFO] Initializing environment for https://github.com/pycqa/flake8.
[INFO] Installing environment for https://github.com/pycqa/isort.
[INFO] Once installed this environment will be reused.
[INFO] This may take a few minutes...
[INFO] Installing environment for https://github.com/pycqa/flake8.
[INFO] Once installed this environment will be reused.
[INFO] This may take a few minutes...
isort (python).......................................(no files to check)Skipped
black................................................(no files to check)Skipped
flake8...............................................(no files to check)Skipped
mypy.................................................(no files to check)Skipped
interrogate..........................................(no files to check)Skipped
pytest-check.............................................................Passed
[main 81450a8] Initialization
 1 file changed, 9 insertions(+)
```

A list of some cool pre-commit hooks can be found [here](https://towardsdatascience.com/4-pre-commit-plugins-to-automate-code-reviewing-and-formatting-in-python-c80c6d2e9f5)

I use:
* [flake8](https://flake8.pycqa.org/en/latest/): code linter to check if the code follows [PEP8](https://peps.python.org/pep-0008/) style guide
* [mypy](https://mypy-lang.org/): static typing verifier
* [isort](https://pycqa.github.io/isort/): to sort my imports appropriately
* [black](https://black.readthedocs.io/en/stable/): to autoformat my code
* [interrogate](https://interrogate.readthedocs.io/en/latest/): to check if all my pieces of code are documented
* [pytest](docs.pytest.org): to run tests (this one is controversial as many programmers prefer to test code serverside. I start with local verification and when the tests are becoming heavy move pytest to server-side CI/CD pipeline).


### Step 5: pyproject.toml: Common project configuration

### Step 6: (direnv) Environment variables autoloadding from file

Context: [Documentation](https://direnv.net/)

Some projects use environment variables to store important configuration data. 
We can use direnv to load those variables every time we enter a given folder (and "unload" them if we move to another one).

These way we can forget about exporting, e.g., AWS credentials every computer reboot.

a) Install direnv: `curl -sfL https://direnv.net/install.sh | bash`

b) [Hook into your shell](https://direnv.net/docs/hook.html)

c) Store your variables into `.envrc` file (remember to add it to `.gitignore` as it may contain data that you should not share!)

```bash
# Create a new folder for demo purposes.
$ mkdir ~/my-project
$ cd ~/my-project

# Show that the FOO environment variable is not loaded.
$ echo ${FOO-nope}
nope

# Create a new .envrc. This file is bash code that is going to be loaded by
# direnv.
$ echo export FOO=foo > .envrc
.envrc is not allowed

# The security mechanism didn't allow to load the .envrc. Since we trust it,
# let's allow its execution.
$ direnv allow .
direnv: reloading
direnv: loading .envrc
direnv export: +FOO

# Show that the FOO environment variable is loaded.
$ echo ${FOO-nope}
foo

# Exit the project
$ cd ..
direnv: unloading

# And now FOO is unset again
$ echo ${FOO-nope}
nope
```