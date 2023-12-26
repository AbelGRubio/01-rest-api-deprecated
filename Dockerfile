FROM python:3.12
LABEL authors="agrubio"


# instalamos los requeriments necesarios
COPY requirements.txt .
COPY src .
RUN python -m pip install -r requirements.txt



CMD ["python", "src"]

