import json
import os
import boto3
from PIL import Image
import io

s3_client = boto3.client('s3')
sqs_client = boto3.client('sqs')

bucket_name = os.environ['BUCKET_NAME']
queue_url = os.environ['QUEUE_URL']

def upload_image(event, context):
    try:
        # Retrieve image data from the HTTP request
        image_data = event['body']
        image_name = event['queryStringParameters']['name']
        
        # Upload image to S3 bucket
        s3_client.put_object(Body=image_data, Bucket=bucket_name, Key=image_name)
        
        # Send message to SQS queue for thumbnail generation
        sqs_client.send_message(QueueUrl=queue_url, MessageBody=image_name)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Image uploaded successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def generate_thumbnail(event, context):
    try:
        # Process messages from SQS queue
        for record in event['Records']:
            image_name = record['body']
            thumbnail_name = 'thumbnail_' + image_name
            
            response = s3_client.get_object(Bucket=bucket_name, Key=image_name)
            image_data = response['Body'].read()
            
            # Generate thumbnail
            image = Image.open(io.BytesIO(image_data))
            image.thumbnail((100, 100))
            
            # Convert thumbnail to bytes
            thumbnail_bytes = io.BytesIO()
            image.save(thumbnail_bytes, format='JPEG')
            thumbnail_bytes.seek(0)
            
            # Upload thumbnail to S3 bucket
            s3_client.put_object(Body=thumbnail_bytes, Bucket=bucket_name, Key=thumbnail_name)
    
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Thumbnail generated successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def get_image(event, context):
    try:
        image_name = event['pathParameters']['imageName']
        
        response = s3_client.get_object(Bucket=bucket_name, Key=image_name)
        image_data = response['Body'].read()
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'image/jpeg'  
            },
            'body': image_data
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def get_thumbnail(event, context):
    try:
        image_name = event['pathParameters']['imageName']
        thumbnail_name = 'thumbnail_' + image_name
        
        response = s3_client.get_object(Bucket=bucket_name, Key=thumbnail_name)
        thumbnail_data = response['Body'].read()
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'image/jpeg'  
            },
            'body': thumbnail_data
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
