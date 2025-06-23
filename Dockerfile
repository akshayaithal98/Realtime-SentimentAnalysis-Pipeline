



FROM python:3.10
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
RUN python -c "from transformers import DistilBertTokenizer, DistilBertForSequenceClassification; \
               DistilBertTokenizer.from_pretrained('distilbert-base-uncased-finetuned-sst-2-english'); \
               DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased-finetuned-sst-2-english')"


CMD ["python", "app.py"]