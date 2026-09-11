from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()


class Entity(BaseModel):
    name: str = Field(description="Name of the entity")
    type: str = Field(
        description="Entity type such as PERSON, ORGANIZATION, LOCATION, SCHEME, GROUP, PRODUCT, OTHER"
    )


class EntityList(BaseModel):
    entities: List[Entity]


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

structured_llm = llm.with_structured_output(EntityList)


prompt = ChatPromptTemplate.from_template("""
Extract the important entities from the text.

Allowed entity types:
PERSON
ORGANIZATION
LOCATION
SCHEME
GROUP
PRODUCT
OTHER

Do not create relationships.
Only identify entities.

Text:
{text}
""")


def extract_entities(text):

    chain = prompt | structured_llm

    result = chain.invoke({
        "text": text
    })

    return result.entities