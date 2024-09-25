from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import  ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
import os
import json

load_dotenv()

class Section(BaseModel):
  title: str = Field(description="The title of the section")
  page: int = Field(description="The page number where the section starts")

class Chapter(BaseModel):
  title: str = Field(description="The title of the chapter")
  page: int = Field(description="The page number where the chapter starts")
  sections: List[Section] = Field(description="List of sections in the chapter")

class TableOfContents(BaseModel):
  chapters: List[Chapter] = Field(description="List of chapters in the table of contents")

parser = PydanticOutputParser(pydantic_object=TableOfContents)

def handler(event, context):
  """
  Lambda function handler to process the input text and extract the table of contents.
  
  :param event: The event dict containing the input
  :param context: The context object provided by AWS Lambda
  :return: A dict containing the status code, headers, and the JSON response
  """
  try:
    body = json.loads(event.get('body', '{}'))
    text = body.get('text', '')

    if not text:
      raise ValueError("No text provided in the input")

    print(body)

    text = body['text']

    chat = ChatOpenAI(
      openai_api_key=os.getenv("OPENAI_API_KEY"),
      model_name="gpt-3.5-turbo",
      temperature=0,    
    )

    template = """テキストの中から目次を探し、指定された形式に変換してください。
目次の各項目には、章、セクション、ページ番号を含めてください。
目次が見つからない場合は、空のリストを返してください。

本文：
{content}

上記の例を参考に、以下の形式で出力してください：
{format_instructions}
"""

    prompt = ChatPromptTemplate.from_template(template).partial(
      format_instructions=parser.get_format_instructions()
    )

    chain = LLMChain(
      llm=chat,
      prompt=prompt,
      output_parser=parser
    )

    result = chain.invoke({"content": text})

    toc_dict = result['text'].model_dump()

    return {
      "statusCode": 200,
      "headers": {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",  # すべてのオリジンを許可
          "Access-Control-Allow-Headers": "Content-Type",
          "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
      },
      "body": json.dumps(toc_dict, ensure_ascii=False)
    }
  except Exception as e:
    return {
        "statusCode": 500,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",  # エラーレスポンスにも追加
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        "body": json.dumps({"error": str(e)}, ensure_ascii=False)
    }