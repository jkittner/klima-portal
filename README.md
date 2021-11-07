[![ci](https://github.com/theendlessriver13/klima/actions/workflows/CI.yaml/badge.svg)](https://github.com/theendlessriver13/klima/actions/workflows/CI.yaml)

# klima-portal

data portal for displaying the measurements collected during the MeMoI course in the summer term of 2021.

## setup

- install the dependencies and start the development server

```console
virtualenv venv -ppy39
venv/bin/pip install -r requirements.txt
venv/bin/python -m portal.app
```

- visit the app at `http://127.0.0.1:5000`
