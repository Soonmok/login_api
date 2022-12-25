FROM python:3.7

COPY app /workspaces/app
COPY requirements.txt /workspaces/app/requirements.txt

WORKDIR /workspaces/app
RUN pip install -r requirements.txt