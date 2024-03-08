from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory, FileChatMessageHistory
from langchain.prompts import MessagesPlaceholder, HumanMessagePromptTemplate, ChatPromptTemplate
from dotenv import load_dotenv
import os
import json

load_dotenv()

json_file = 'chat_history.json'

with open(json_file, 'w') as f:
  f.write('[]')

def handler(event, context):

  chat = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
  )

  prompt = ChatPromptTemplate(
    input_variables=["content", "chat_history"],
    messages=[
      MessagesPlaceholder(variable_name="chat_history"),
      HumanMessagePromptTemplate.from_template("{content}")
    ]
  )

  memory = ConversationBufferMemory(
    chat_memory=FileChatMessageHistory("chat_history.json"),
    memory_key="chat_history",
    return_messages=True
  )

  chain = LLMChain(
    llm=chat,
    prompt=prompt,
    memory=memory,
  )

  print(event["body"]["input"])

  result = chain.invoke({"content": event["body"]["input"]})

  return {
    "statusCode": 200,
    "headers": {
      "Content-Type": "application/json"
    },
    "body": json.dumps(result['text'])
  }
