import gzip
import pickle

with gzip.open("bmo1_brain.pbz2", "rb") as f:
    graph = pickle.load(f)
    
    # In Rhasspy's graph, intent names are stored in the 'intent_metadata'
    intents = set()
    for node, data in graph.nodes(data=True):
        if "intent_metadata" in data:
            for meta in data["intent_metadata"]:
                intents.add(meta.intent_name)
    
    print("--- BMO BRAIN CONTENTS ---")
    if not intents:
        print("❌ The brain is EMPTY. No intents found.")
    else:
        for i in intents:
            print(f"✅ Intent: {i}")
    print("--------------------------")