import argparse

from src.search.engine import SearchEngine


def create_parser():
    parser = argparse.ArgumentParser(
        prog="zero-deps",
        description="Zero Dependency Search Engine"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    # Add
    add_parser = subparsers.add_parser(
        "add",
        help="Add a document"
    )
    add_parser.add_argument("document_id", type=int)
    add_parser.add_argument("text")

    # Search
    search_parser = subparsers.add_parser(
        "search",
        help="Search documents"
    )
    search_parser.add_argument("query")

    # Update
    update_parser = subparsers.add_parser(
        "update",
        help="Update a document"
    )
    update_parser.add_argument("document_id", type=int)
    update_parser.add_argument("text")

    # Remove
    remove_parser = subparsers.add_parser(
        "remove",
        help="Remove a document"
    )
    remove_parser.add_argument("document_id", type=int)
        # Stats
    subparsers.add_parser(
        "stats",
        help="Show index statistics"
    )

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    engine = SearchEngine("data/index.json")

    if args.command == "add":
        engine.add_document(args.document_id, args.text)
        print(f"Document {args.document_id} added.")

    elif args.command == "search":
        results = engine.search(args.query)

        if not results:
            print("No documents found.")
            return

        print("Search results:")
        for document_id in sorted(results):
            print(f"- Document {document_id}")

    elif args.command == "update":
        engine.update_document(args.document_id, args.text)
        print(f"Document {args.document_id} updated.")

    elif args.command == "remove":
        engine.remove_document(args.document_id)
        print(f"Document {args.document_id} removed.")
    elif args.command == "stats":
        document_count = len(engine.index.term_frequencies)
        unique_terms = len(engine.index.index)

        total_postings = sum(
            len(document_ids)
            for document_ids in engine.index.index.values()
        )

        print("Index Statistics")
        print("----------------")
        print(f"Documents       : {document_count}")
        print(f"Unique terms    : {unique_terms}")
        print(f"Index entries   : {total_postings}")
        print(f"Cache capacity  : {engine.index.cache.capacity}")

if __name__ == "__main__":
    main()