# import unittest
# from unittest.mock import MagicMock
# from src.handler import upload_image, generate_thumbnail, get_image, get_thumbnail

# class TestHandler(unittest.TestCase):

#     def setUp(self):
        
#         self.s3_client = MagicMock()

#         self.sqs_client = MagicMock()

#     def test_upload_image(self):
        
#         event = {
#             "body": "base64_encoded_image_data"
#         }

#         response = upload_image(event, None, s3_client=self.s3_client, sqs_client=self.sqs_client)

#         self.s3_client.upload_file.assert_called_once()

#         self.sqs_client.send_message.assert_called_once()

#         self.assertIn("statusCode", response)
#         self.assertIn("body", response)
#         self.assertIn("message", response["body"])

#     def test_generate_thumbnail(self):
        
#         event = {
#             "Records": [
#                 {
#                     "s3": {
#                         "bucket": {"name": "test-bucket"},
#                         "object": {"key": "test-image.jpg"}
#                     }
#                 }
#             ]
#         }

        
#         generate_thumbnail(event, None, s3_client=self.s3_client)

#         self.s3_client.download_file.assert_called_once()
#         self.s3_client.upload_file.assert_called_once()

#     def test_get_image(self):
        
#         event = {
#             "pathParameters": {"imageName": "test-image.jpg"}
#         }

#         response = get_image(event, None, s3_client=self.s3_client)

#         self.assertIn("statusCode", response)
#         self.assertIn("body", response)
#         self.assertIn("image_data", response["body"])

#     def test_get_thumbnail(self):
#         event = {
#             "pathParameters": {"imageName": "test-image-thumbnail.jpg"}
#         }

#         response = get_thumbnail(event, None, s3_client=self.s3_client)

#         self.assertIn("statusCode", response)
#         self.assertIn("body", response)
#         self.assertIn("thumbnail_data", response["body"])

# if __name__ == '__main__':
#     unittest.main()
