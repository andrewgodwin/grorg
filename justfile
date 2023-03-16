set dotenv-load := false

@_default:
    just --list

@deploy:
    flyctl deploy

@fmt:
    just --fmt --unstable

@pre-commit:
    pre-commit run --all-files

@up:
    python manage.py runserver

@update:
    pip install -U pip pip-tools
    pip install -U -r requirements.in
    pip-compile requirements.in
