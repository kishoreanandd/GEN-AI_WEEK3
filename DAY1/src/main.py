from document_loader import load_document
from entity_extraction import extract_entities
from relationship_mapping import extract_relationships


file_path = "data/sample.txt"

documents = load_document(file_path)

text = documents[0].page_content


print("========== DOCUMENT ==========")
print(text)


print("\n========== ENTITIES ==========")

entities = extract_entities(text)

for entity in entities:
    print(f"{entity.name} → {entity.type}")


print("\n========== RELATIONSHIPS ==========")

relationships = extract_relationships(text)

for relationship in relationships:
    print(
        f"{relationship.source} "
        f"--[{relationship.relationship}]--> "
        f"{relationship.target}"
    )