import os
import certifi

os.environ["SSL_CERT_FILE"] = certifi.where()

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")


driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


def create_graph(tx):
    query = """
    MERGE (scheme:Scheme {name: "Training to Farmers"})

    MERGE (beneficiary:Beneficiary {name: "Farmers"})

    MERGE (skill:Skill {
        name: "Agricultural knowledge and skills"
    })

    MERGE (scheme)-[:BENEFITS]->(beneficiary)

    MERGE (scheme)-[:IMPROVES]->(skill)
    """

    tx.run(query)


try:
    with driver.session() as session:
        session.execute_write(create_graph)

    print("Graph data inserted successfully!")

except Exception as e:
    print("Insert failed:")
    print(type(e).__name__)
    print(e)

finally:
    driver.close()