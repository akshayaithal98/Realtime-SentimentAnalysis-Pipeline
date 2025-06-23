from flask import Flask,request,jsonify,Blueprint
from google.cloud import bigquery
import json
import base64
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

# import os
#app=Flask(__name__)
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="gcp_learning_service_account.json"

sentiment_analysis_file=Blueprint("sentiment_analysis_file",__name__)

@sentiment_analysis_file.route("/find_sentiment",methods=["POST"])
def receive_pubsub_message():
    try:
        envelope=request.get_json()
        if not envelope:
            return jsonify({"error":"invalid request with no data"}),400
        
        pubsub_msg=envelope.get("message",{})
        if "data" in pubsub_msg:
            #message_data=pubsub_msg["data"]
            decoded_msg = base64.b64decode(pubsub_msg["data"]).decode('UTF-8')
            message_data=json.loads(decoded_msg)
            print(f"Received pubsub push mechanism msg:{message_data}")
            review=message_data.get("review","")
            review_id=message_data.get("review_id")
            print(review,review_id)
            smt=sentiment(review)
            print(f"sentiment is {smt}")
            insert_to_bq(review_id,review,smt)
        else:
            print("pubsub msg has no data field")

        return jsonify({"status":f"message received {review}"}),200 #for acknowledgement
    except Exception as error:
        return jsonify({"status":"failed to process message"}),500

def insert_to_bq(review_id,review,sentiment):
    dataset="python_dataset"
    table_name="reviews"
    client=bigquery.Client()
    query=f"""
    insert into {dataset}.{table_name} (review_id,review,sentiment) values({review_id},'{review}','{sentiment}')
    """
    print(query)
    result=client.query(query)
    print(result)


def sentiment(review):

    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
    model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

    inputs=tokenizer(review,return_tensors='pt',truncation=True,padding=True)
    inputs = tokenizer(review, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits

    predicted_class_id = logits.argmax().item()
    print(predicted_class_id)
    return model.config.id2label[predicted_class_id]
