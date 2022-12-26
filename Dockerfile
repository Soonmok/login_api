FROM python:3.7

COPY app /workspaces/app
COPY requirements.txt /workspaces/requirements.txt
COPY alembic.ini /workspaces/alembic.ini
COPY tests /workspaces/tests

WORKDIR /workspaces
RUN pip install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/workspaces"
