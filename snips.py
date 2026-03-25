import io
import os
from snips_nlu import SnipsNLUEngine


# This file is used to train BMO if ever we wanna add more utterances to the training.json file!
MODEL_PATH = "bmo_trained_engine.bin"

def get_bmo_engine(dataset_path):

    if os.path.exists(MODEL_PATH):
        print("💾 Loading B.MO's existing brain...")
        with io.open(MODEL_PATH, mode="rb") as f:
            engine_bytes = f.read()
        return SnipsNLUEngine.from_bytearray(engine_bytes)
   
    print("🧠 Training a new brain for B.MO...")
    with io.open(dataset_path, str("r"), encoding="utf-8") as f:
        dataset = json.load(f)
    
    engine = SnipsNLUEngine()
    engine.fit(dataset)
    
    with io.open(MODEL_PATH, mode="wb") as f:
        f.write(engine.to_bytearray())
        
    return engine