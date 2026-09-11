from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()


class Relationship(BaseModel):
    source: str = Field(
        description="Source entity name"
    )

    relationship: str = Field(
        description="Relationship between the two entities"
    )

    target: str = Field(
        description="Target entity name"
    )


class RelationshipList(BaseModel):
    relationships: List[Relationship]


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

structured_llm = llm.with_structured_output(
    RelationshipList
)


prompt = ChatPromptTemplate.from_template("""
You are a knowledge graph relationship extraction system.

Extract relationships between the entities found in the text.

Rules:

1. Only create relationships supported by the text.
2. Do not invent relationships.
3. Use short, clear relationship names.
4. Use uppercase relationship names.
5. Return source, relationship, and target.

Example:

Text:
The Training to Farmers scheme provides training to farmers.

Output:
source = Training to Farmers
relationship = HAS_BENEFICIARY
target = Farmers

Text:
{text}
""")


def extract_relationships(text):

    chain = prompt | structured_llm

    result = chain.invoke({
        "text": text
    })

    return result.relationships