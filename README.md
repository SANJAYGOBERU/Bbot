💰 Banking Bot Assistant – Powered by AWS Lex & DynamoDB
🤖 AI-Powered Financial Assistant for Secure and Instant Banking
This project is an intelligent Banking Bot Assistant built using Amazon Lex, integrated with AWS Lambda and Amazon DynamoDB to provide real-time, secure account balance inquiries through natural language interactions.


🚀 Features
✅ Natural Language Processing (NLP) – Uses Amazon Lex for understanding user queries
✅ Secure Data Access – Retrieves account details securely from DynamoDB
✅ Serverless Architecture – Uses AWS Lambda for backend processing
✅ Instant Financial Updates – Provides real-time account balances
✅ Highly Scalable – Works seamlessly across multiple users

🏗️ Architecture Diagram
rust
Copy
Edit
User -> Amazon Lex -> AWS Lambda -> DynamoDB -> Response
AWS Services Used:
Amazon Lex – For chatbot functionality
AWS Lambda – For backend business logic
Amazon DynamoDB – For securely storing account details
Amazon API Gateway (Optional) – If integrating with external applications
Amazon CloudWatch – For monitoring and debugging
🛠️ Setup & Deployment
1️⃣ Clone the Repository
bash
Copy
Edit
git clone https://github.com/yourusername/banking-bot.git
cd banking-bot
2️⃣ Configure AWS Credentials
Ensure you have AWS CLI configured:

bash
Copy
Edit
aws configure
Set up IAM permissions for Lex, Lambda, and DynamoDB.

3️⃣ Create DynamoDB Table
Table Name: bbottable
Primary Key	Type
accountnumber	String
balance	String
Example entry:

json
Copy
Edit
{
  "accountnumber": { "S": "123456789" },
  "balance": { "S": "$5,000" }
}
4️⃣ Deploy AWS Lambda Function
Navigate to AWS Lambda
Create a new Lambda function
Upload lambda_function.py
Set runtime to Python 3.9+
Attach the required IAM role for DynamoDB access
5️⃣ Configure Amazon Lex
Create a new bot in Amazon Lex
Add Intent: Balancebot
Define a slot: acc-num (Type: AMAZON.Number)
Integrate it with the Lambda function
📝 Lambda Function Code
python
Copy
Edit
import json
import boto3

client = boto3.client('dynamodb')

def get_slots(intent_request):
    return intent_request['sessionState']['intent']['slots']

def get_slot(intent_request, slotName):
    slots = get_slots(intent_request)
    return slots.get(slotName, {}).get('value', {}).get('interpretedValue')

def get_session_attributes(intent_request):
    return intent_request['sessionState'].get('sessionAttributes', {})

def close(intent_request, session_attributes, fulfillment_state, message):
    intent_request['sessionState']['intent']['state'] = fulfillment_state
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {'type': 'Close'},
            'intent': intent_request['sessionState']['intent']
        },
        'messages': [message],
        'sessionId': intent_request['sessionId'],
        'requestAttributes': intent_request.get('requestAttributes')
    }

def Balancebot(intent_request):
    session_attributes = get_session_attributes(intent_request)
    acc_num = get_slot(intent_request, 'acc-num')

    if not acc_num:
        return close(intent_request, session_attributes, "Failed", 
                     {'contentType': 'PlainText', 'content': "Account number is required."})

    try:
        response = client.get_item(
            TableName='bbottable',
            Key={'accountnumber': {'S': acc_num}}
        )

        if 'Item' in response and 'balance' in response['Item']:
            balance = response['Item']['balance']['S']
            message = {'contentType': 'PlainText', 'content': f'Thank you for using BALANCE BOT. Your account balance is: {balance}'}
            return close(intent_request, session_attributes, "Fulfilled", message)
        else:
            return close(intent_request, session_attributes, "Failed", 
                         {'contentType': 'PlainText', 'content': "Account not found."})
    
    except Exception as e:
        return close(intent_request, session_attributes, "Failed", 
                     {'contentType': 'PlainText', 'content': f"Error fetching data: {str(e)}"})

def dispatch(intent_request):
    intent_name = intent_request['sessionState']['intent']['name']
    if intent_name == 'Balancebot':
        return Balancebot(intent_request)
    raise Exception(f'Intent {intent_name} not supported')

def lambda_handler(event, context):
    response = dispatch(event)
    print(json.dumps(event, indent=2))  # Log input for debugging
    return response
📌 How to Use
Open Amazon Lex and start a conversation
Ask:
arduino
Copy
Edit
"What is my account balance?"
The bot will ask for your account number
Enter the account number: 123456789
The bot will fetch your balance from DynamoDB and respond
🔒 Security Considerations
Encrypt sensitive data using AWS KMS
Use IAM roles to restrict access to Lambda & DynamoDB
Enable API Gateway authentication if integrating with a web app
Use AWS CloudWatch Logs to monitor requests
🛠️ Future Enhancements
✅ Multi-User Support with Authentication
✅ Add Transaction History Retrieval
✅ Voice-based interactions with Alexa Integration
✅ UI Dashboard with React or Vue.js
🤝 Contributing
Contributions are welcome! Please follow these steps:

Fork the repository
Create a feature branch (git checkout -b feature-xyz)
Commit changes (git commit -m "Added feature xyz")
Push to the branch (git push origin feature-xyz)
Open a Pull Request
