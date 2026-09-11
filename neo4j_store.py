import os
import certifi

os.environ["SSL_CERT_FILE"] = certifi.where()

from dotenv import load_dotenv
from neo4j import GraphDatabase

from graph_data import entities, relationships

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")


driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


def create_entity(tx, entity):
    query = """
    MERGE (e:Entity {
        name: $name,
        type: $type
    })
    """

    tx.run(
        query,
        name=entity["name"],
        type=entity["type"]
    )


def create_relationship(tx, relationship):
    query = """
    MATCH (source:Entity {
        name: $source,
        type: $source_type
    })

    MATCH (target:Entity {
        name: $target,
        type: $target_type
    })

    MERGE (source)-[r:RELATED_TO {
        type: $relationship
    }]->(target)
    """

    tx.run(
        query,
        source=relationship["source"],
        source_type=relationship["source_type"],
        target=relationship["target"],
        target_type=relationship["target_type"],
        relationship=relationship["relationship"]
    )


try:

    with driver.session() as session:

        for entity in entities:
            session.execute_write(
                create_entity,
                entity
            )

        for relationship in relationships:
            session.execute_write(
                create_relationship,
                relationship
            )

    print("Entities and relationships stored successfully!")

except Exception as e:

    print("Graph storage failed:")
    print(type(e).__name__)
    print(e)

finally:
    driver.close()