from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Instructions for generating these keys here:
# https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html
# Ideally, "use temporary security credentials (IAM roles) instead of creating long-term credentials like access keys"
S3_BUCKET = getenv("S3_BUCKET", None)
S3_KEY = getenv("S3_KEY", None)
S3_SECRET = getenv("S3_SECRET", None)
assert S3_BUCKET
assert S3_KEY
assert S3_SECRET
