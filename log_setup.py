
import logging
import time
import boto3
import watchtower
import json

# AWS credentials and region for CloudWatch logging
AWS_ACCESS_KEY_ID = '' 
AWS_SECRET_ACCESS_KEY = ''  
AWS_REGION = ''  

# Create a boto3 CloudWatch client with the explicit credentials
cloudwatch_client = boto3.client(
    'logs',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# Create a logger
logger = logging.getLogger('aws_logger')
logger.setLevel(logging.DEBUG)  # Set the log level to DEBUG so all levels of logs are captured

# Define a custom JSON formatter
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_message = {
            'timestamp': self.formatTime(record, self.datefmt),
            'level': record.levelname,
            'message': record.getMessage(),
            'logger': record.name,
            'filename': record.filename,
            'line_no': record.lineno,
            'func_name': record.funcName,
        }
        return json.dumps(log_message)

# Create log group if it does not exist
log_group = 'MyLogGroupForLogging'
log_stream = 'MyLogStreamForLogging'



# Create a Watchtower CloudWatch Log Handler which will send the logs to CloudWatch
cloudwatch_handler = watchtower.CloudWatchLogHandler(
    log_group=log_group, 
    stream_name=log_stream,  
    boto3_client=cloudwatch_client 
)

# Set the custom JSON formatter for the CloudWatch log handler
cloudwatch_handler.setFormatter(JSONFormatter())

# Add the CloudWatch handler to the logger, so logs will be sent to CloudWatch
logger.addHandler(cloudwatch_handler)


try:
    while True:
        logger.debug('This is a DEBUG message') 
        logger.info('This is an INFO message')  
        logger.warning('This is a WARNING message')  
        logger.error('This is an ERROR message')  
        logger.critical('This is a CRITICAL message')  
        time.sleep(5)  
except KeyboardInterrupt:
    print("Logging interrupted. Exiting.")
