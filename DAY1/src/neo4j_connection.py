import os
import certifi

os.environ["SSL_CERT_FILE"] = certifi.where()

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

print("URI:", URI)
print("USERNAME:", USERNAME)
print("PASSWORD loaded:", bool(PASSWORD))
print("CA bundle:", certifi.where())

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

try:
    driver.verify_connectivity()
    print("Neo4j connection successful!")

except Exception as e:
    print("Connection failed:")
    print(type(e).__name__)
    print(e)

finally:
    driver.close()