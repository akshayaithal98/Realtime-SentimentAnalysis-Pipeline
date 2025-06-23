# Review Sentiment Analysis Pipeline
## use command+shift+v to view this file.
## Overview
This project sets up a sentiment analysis pipeline for user reviews using Google Cloud Platform (GCP) services. It consists of a publisher API to send reviews and a subscriber API to process reviews, perform sentiment analysis, and store results in BigQuery.

## Project Steps

### 1. Set Up GCP Resources
- Create a **Pub/Sub topic** to receive reviews, before this have a message schema created.
- Create a **BigQuery table** to store processed review data.
- provide permissions for pubsub, bq, cloud function,artifact registry and all these apis should be enabled.


### 2. Develop APIs
- Write the **Review Publisher API** to send reviews to a Pub/Sub topic.
- Write the **Review Subscriber API** to receive reviews, perform sentiment analysis, and insert results into BigQuery.



### 3. Connect Publisher and Subscriber
- The publisher API sends reviews to the Pub/Sub topic.
- The Pub/Sub topic pushes messages to the subscriber endpoint.
- The subscriber receives reviews via a push request, processes them, performs sentiment analysis, and inserts them into BigQuery.

### 4. Authentication Setup
- When running **locally**, use a **service account JSON key**.
- When running on **GCP**, authentication is handled automatically.

### 5. Deploy API using Docker
- Create a folder in **Google Cloud Shell** with the following structure:
  ```
  /project-folder
    ├── app.py
    ├── routes/
    ├── requirements.txt
    ├── Dockerfile
  ```
- Build the Docker image.

### 6. Push Docker Image to Artifact Registry
- Upload the Docker image to **Google Artifact Registry**.

### 7. Deploy API to Cloud Run
- Deploy the subscriber API to **Cloud Run**.
- Cloud Run provides a public endpoint like https://sa-image-48111.us-central1.run.app

### 8. Link Subscriber to Pub/Sub
- Add the **Cloud Run subscriber endpoint** as a **subscriber** to the Pub/Sub topic.

### 9. Test APIs
- Use **Postman** or `curl` to test the APIs and verify real-time processing.

---

## Docker Deployment Steps

### Step 1: Build Docker Image
```sh
docker build -t sentiment_image .
```

### Step 2: Run Locally
```sh
docker run -p 8080:8080 sentiment_image
```

### Step 3: Upload Image to Cloud Shell (if built locally)
```sh
docker save -o sentiment_image.tar sentiment_image
```
Upload to **Google Cloud Shell**, then load and tag the image:
```sh
docker load -i sentiment_image.tar
```

### Step 4: Tag and Push Image to Artifact Registry
```sh
docker tag sentiment_image us-central1-docker.pkg.dev/eloq-theme-44444-t2/my-repo/sentiment_image

docker push us-central1-docker.pkg.dev/eloq-theme-44444-t2/my-repo/sentiment_image
```

### Step 5: Test the Image Locally with `curl`
```sh
curl -X POST "http://127.0.0.1:8080/post_review" \
     -H "Content-Type: application/json" \
     -d '{"review":"good","review_id":3}'
```

---
