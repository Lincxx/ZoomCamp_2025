FROM python:3.9

RUN pip install --upgrade pip
RUN pip install pandas

WORKDIR /app
COPY pipeline.py pipeline.py

# ENTRYPOINT [ "bash" ]
ENTRYPOINT [ "python", "pipeline.py" ]