
import json
from pathlib import Path

# Plugin configuration
BASE_DIR = Path(__file__).parent / "knowledge_base"

ALLOWED_EXTENSIONS = {".txt", ".md", ".py", ".json"}


# 1. EXECUTION LOGIC
def search_files(query: str, max_results: int = 5) -> str:
    """Search filenames and file contents for a query."""

    if not query.strip():
        return json.dumps({"error": "Query cannot be empty"})

    max_results = max(1, min(max_results, 10))

    if not BASE_DIR.exists():
        return json.dumps({"error": "Knowledge base not found"})

    results = []
    query_lower = query.lower()

    for file_path in BASE_DIR.rglob("*"):
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue

        try:
            content = file_path.read_text(
                encoding="utf-8",
                errors="replace"
            )
        except OSError:
            continue

        filename_match = query_lower in file_path.name.lower()
        content_match = query_lower in content.lower()

        if filename_match or content_match:
            results.append({
                "filename": file_path.name,
                "path": str(file_path.relative_to(BASE_DIR)),
                "match_in": (
                    "filename and content"
                    if filename_match and content_match
                    else "filename"
                    if filename_match
                    else "content"
                ),
                "snippet": (
                    content[:200].replace("\n", " ")
                    if content_match else ""
                )
            })

        if len(results) >= max_results:
            break

    # 2. STRUCTURED RETURN FORMAT
    return json.dumps({
        "query": query,
        "count": len(results),
        "results": results
    }, indent=2)

# DEMO: Execute the plugin directly
if __name__ == "__main__":

    print("\nPlugin Execution:")
    output = search_files("Python")
    print(output)
