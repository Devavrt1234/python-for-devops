from flask import Flask, jsonify
import boto3
from botocore.exceptions import ClientError
import json
import os

app = Flask(__name__)

def get_secret():
    secret_name = os.environ.get("SECRET_NAME", "python-app-secret")
    region_name = os.environ.get("AWS_REGION", "us-east-2")

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']
    return json.loads(secret)

@app.route('/')
def hello_world():
    try:
        secret = get_secret()
        return jsonify({
            "message": "Hello, World!",
            "secret": secret
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)



