from src.search.engine import SearchEngine


def main():
    engine = SearchEngine()

    while True:
        print("\n================================")
        print("       ZERO-DEPS SEARCH")
        print("================================")
        print("1. Add document")
        print("2. Search")
        print("3. Update document")
        print("4. Remove document")
        print("5. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            document_id = int(input("Document ID: "))
            text = input("Text: ")

            engine.add_document(document_id, text)

            print("Document added successfully.")

        elif choice == "2":
            query = input("Search query: ")

            results = engine.search(query)

            print(f"Results: {results}")

        elif choice == "3":
            document_id = int(input("Document ID: "))
            text = input("New text: ")

            engine.update_document(document_id, text)

            print("Document updated successfully.")

        elif choice == "4":
            document_id = int(input("Document ID: "))

            engine.remove_document(document_id)

            print("Document removed successfully.")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1-5.")


if __name__ == "__main__":
    main()