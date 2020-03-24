import boto3

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    obj = s3.get_object(Bucket=bucket, Key=key)
    
    rows = obj['Body'].read().split('\n')
    table = dynamodb.Table('Recipes')
    
    with table.batch_writer() as batch:
        for row in rows:
            try:
                index = row.split(',')[0]
                recipe  = row.split(',')[1]
                food = row.split(',')[2]
                calorie = row.split(',')[3]
                if (index=="" or recipe=="" or food=="" or calorie==""):
                    pass
                else:
                    batch.put_item(Item={
                        'index': index,
                        'recipe': recipe,
                        'food': food,
                        'calorie': calorie
                })
            except:
                pass
    
