import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--detect-only", action="store_true")
    args = parser.parse_args()

    if args.detect_only:
        print("Detecting redundant chunks...")
    else:
        print("Merging redundant chunks...")

if __name__ == "__main__":
    main()
