FROM python:3.8.2
 
COPY . /app
WORKDIR /app
 
RUN pip install -r requirements.txt
EXPOSE 5000
 
CMD ["python3", "app.py"]