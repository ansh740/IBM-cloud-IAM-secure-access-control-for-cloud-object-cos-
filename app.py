from flask import Flask, render_template, jsonify
import ibm_boto3
from ibm_botocore.client import Config

app = Flask(__name__)

# IBM COS configuration
cos = ibm_boto3.client(
    "s3",
    ibm_api_key_id="lrZevqsL5z4nej_4lsmkiFEtZFHlE1tu2TUVgKpQhIkIY",
    ibm_service_instance_id="crn:v1:bluemix:public:cloud-object-storage:global:a/3917e539fefc419a8fd3fac5b76b4a45:7cd17ac8-06a8-4258-8e3e-11b731bdb83f::",
    config=Config(signature_version="oauth"),
    endpoint_url="https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints"
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get-file-url")
def get_file_url():
    try:
        url = cos.generate_presigned_url(
            'get_object',
            Params={'Bucket': 'secure-data-bucket', 'Key': 'index.html'},
            ExpiresIn=600
        )
        return jsonify({"url": url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
