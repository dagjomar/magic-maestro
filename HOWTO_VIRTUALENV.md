# How to setup virtual environment

```bash
# Make sure your python version is <= 3.12 when creating the virtual environment
# or use another way to get the specific python version
python3 -m venv venv
source ./venv/bin/activate
```

### Alternative way for OSX when having a specific python version installed using brew
```bash
/opt/homebrew/bin/python3.12 -m venv venv
source ./venv/bin/activate
```

### Optional
Add a .envrc file to the root directory to automatically load the environment variables from the .env file.

```bash
echo "source ./venv/bin/activate" > .envrc
direnv allow
```
