FROM python:3.10-alpine
EXPOSE 8000/tcp
WORKDIR /opt/app
ADD *.py .
RUN install requirements
CMD ["uvicorn", "--port", "8000" "main:app"]