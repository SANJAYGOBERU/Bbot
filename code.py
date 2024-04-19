import json
import boto3
client = boto3.client('dynamodb')

def get_slots(intent_request):
    return intent_request['sessionState']['intent']['slots']
    
def get_slot(intent_request, slotName):
    slots = get_slots(intent_request)
    if slots is not None and slotName in slots and slots[slotName] is not None:
        return slots[slotName]['value']['interpretedValue']
    else:
        return None 
        
def get_session_attributes(intent_request):
    sessionState = intent_request['sessionState']
    if 'sessionAttributes' in sessionState:
        return sessionState['sessionAttributes']

    return {}
    
def close(intent_request, session_attributes, fulfillment_state, message):
    intent_request['sessionState']['intent']['state'] = fulfillment_state
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close'
            },
            'intent': intent_request['sessionState']['intent']
        },
        'messages': [message],
        'sessionId': intent_request['sessionId'],
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }
    
def Balancebot(intent_request):
    session_attributes = get_session_attributes(intent_request)
    slots = get_slots(intent_request)
    GetItem = client.get_item(
    TableName='bbottable',
    Key={
        'accountnumber': {
            'S': (intent_request['sessionState']['intent']['slots']['acc-num']['value']['originalValue'])
            }
        }
    )
    message =  {
            'contentType': 'PlainText',
            'content': 'Thank you for using BALANCE BOT  your account balance is : ' + GetItem['Item']['balance']['S']
#            'content': 'text'
        }
    fulfillment_state = "Fulfilled"    
    return close(intent_request, session_attributes, fulfillment_state, message)
    
   
def dispatch(intent_request):
    intent_name = intent_request['sessionState']['intent']['name']
    response = None
    # Dispatch to your bot's intent handlers
    if intent_name == 'Balancebot':
        return Balancebot(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')

def lambda_handler(event, context):
    response = dispatch(event)
    print(event)
    return response
  
