entities = [
    {
        "name": "Training to Farmers",
        "type": "Scheme"
    },
    {
        "name": "Farmers",
        "type": "Beneficiary"
    },
    {
        "name": "Agricultural knowledge and skills",
        "type": "Skill"
    }
]


relationships = [
    {
        "source": "Training to Farmers",
        "source_type": "Scheme",
        "relationship": "BENEFITS",
        "target": "Farmers",
        "target_type": "Beneficiary"
    },
    {
        "source": "Training to Farmers",
        "source_type": "Scheme",
        "relationship": "IMPROVES",
        "target": "Agricultural knowledge and skills",
        "target_type": "Skill"
    }
]