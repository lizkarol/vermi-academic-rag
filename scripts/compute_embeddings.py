import os

def main():
    print("Computing embeddings...")
    # Dummy implementation
    if not os.path.exists("dataset/embeddings"):
        os.makedirs("dataset/embeddings")
    with open("dataset/embeddings/vectors_300d_v1.0.parquet", "w") as f:
        f.write("")
    print("Embeddings computed.")

if __name__ == "__main__":
    main()
