import lancedb

def main():
    db = lancedb.connect("data/sample-lancedb")
    # ...
    print("Loaded data with LanceDB.")

if __name__ == "__main__":
    main()
