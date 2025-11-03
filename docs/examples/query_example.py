import lancedb

def main():
    db = lancedb.connect("data/sample-lancedb")
    # ...
    print("Query example.")

if __name__ == "__main__":
    main()
