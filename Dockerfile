FROM alpine:3.23.4

WORKDIR /app/

RUN apk --no-cache add python3 bash

RUN python -m venv /app/venv/
ENV PATH="/app/venv/bin:$PATH"

COPY dist/ /temp/dist/

RUN pip install /temp/dist/*.whl
