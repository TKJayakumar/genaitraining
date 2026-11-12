import os
from sentence_transformers import SentenceTransformer


# 1. Define your 10 sample sentences
sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "A fast amber fox leaps across the sleeping hound.",
    "How do I reset my account password?",
    "I forgot my login credentials, can you help me recover them?",
    "Machine learning models require clean training data.",
    "Deep neural networks perform best with large datasets.",
    "The local market sells fresh vegetables and fruits.",
    "Farmers bring organic produce to the town square every morning.",
    "Quantum computing leverages superposition and entanglement.",
    "Next-generation processors use advanced sub-nanometer architecture.",
]


open_source_model = SentenceTransformer("all-MiniLM-L6-v2")


os_embeddings = open_source_model.encode(sentences).tolist()


all_labels = [f"OpenSource: {s}" for s in sentences]
all_models = ["all-MiniLM-L6-v2"] * len(sentences)


os.makedirs("projector_data", exist_ok=True)


vectors_path = "projector_data/vectors.tsv"


with open(vectors_path, "w", encoding="utf-8") as f:
    for emb in os_embeddings:
         f.write("\t".join(map(str, emb)) + "\n")


metadata_path = "projector_data/metadata.tsv"
with open(metadata_path, "w", encoding="utf-8") as f:
    f.write("Sentence\tModel\n")


    for label, model_type in zip(all_labels, all_models):
        f.write(f"{label}\t{model_type}\n")


print(f"Successfully generated files at '{vectors_path}' and '{metadata_path}'!")


 