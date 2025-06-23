from flask import Flask,request,jsonify,Blueprint
from  google.cloud import pubsub_v1
import json

# import os
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="gcp_learning_service_account.json"


GCP_PROJECT_ID="my_project"

#app=Flask(__name__)

post_reviews_file=Blueprint("post_reviews_file",__name__)

@post_reviews_file.route("/post_review",methods=["POST"])
def post_reviews():
    data=request.get_json()
    review=data["review"]
    review_id=data["review_id"]

    message={"review_id":review_id,"review":review}

    client=pubsub_v1.PublisherClient()
    topic=client.topic_path(GCP_PROJECT_ID,"reviews_topic")
    message=json.dumps(message)
    pubsub_msg=message.encode('UTF-8')
    future=client.publish(topic,pubsub_msg)
    print(future.result())
    return jsonify({"output":future.result()})

