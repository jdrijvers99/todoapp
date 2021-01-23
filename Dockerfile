FROM python:3.8-alpine
WORKDIR /app
COPY requirements.txt /app
COPY main.py /app
COPY templates /app/templates
COPY static /app/static
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD ["main.py"]