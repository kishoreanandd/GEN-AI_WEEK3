import os
import certifi

# Fix SSL certificate issue
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


def get_beneficiaries(tx, scheme_name):
    query = """
    MATCH (scheme:Entity {name: $scheme_name})
          -[:RELATED_TO {type: "BENEFITS"}]->
          (beneficiary:Entity)
    RETURN beneficiary.name AS beneficiary
    """

    result = tx.run(query, scheme_name=scheme_name)

    return [record["beneficiary"] for record in result]

def get_improvements(tx, scheme_name):
    query = """
    MATCH (scheme:Entity {name: $scheme_name})
          -[:RELATED_TO {type: "IMPROVES"}]->
          (target:Entity)
    RETURN target.name AS improvement
    """

    result = tx.run(query, scheme_name=scheme_name)

    return [record["improvement"] for record in result]

try:
    with driver.session() as session:

        beneficiaries = session.execute_read(
            get_beneficiaries,
            "Training to Farmers"
        )

        improvements = session.execute_read(
            get_improvements,
            "Training to Farmers"
        )

        print("\nImprovements:")

        for improvement in improvements:
            
            print("-", improvement)
        print("Beneficiaries:")

        for person in beneficiaries:
            print("-", person)

except Exception as e:
    print("Query failed:")
    print(type(e).__name__)
    print(e)

finally:
    driver.close()