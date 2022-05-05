FROM python:3.9

RUN pip install pipenv
WORKDIR app/

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system
COPY . ./

CMD ["python", "main.py"]