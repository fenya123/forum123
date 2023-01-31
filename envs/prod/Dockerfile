FROM python:3.10-slim

WORKDIR /forum123

# Setup and activate python3.10 virtual environment. It will allow us to avoid this warning from pip:
#     WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system
#     package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
RUN python3.10 -m venv .venv
ENV PATH="/forum123/.venv/bin:$PATH"

COPY requirements.txt requirements-prod.txt ./

RUN apt-get update \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
                                  -r requirements-prod.txt

COPY . ./

ENV FLASK_APP=forum123
