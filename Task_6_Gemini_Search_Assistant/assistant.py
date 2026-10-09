import os
import sys
from typing import Optional

from dotenv import load_dotenv
from google import genai

# Load .env first so GEMINI_API_KEY and an optional GEMINI_MODEL override are
# picked up before they are read below.
load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")


def build_client() -> genai.Client:
    """Create a Gemini client using a local environment variable."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Copy .env.example to .env and add your API key."
        )
    return genai.Client(api_key=api_key)


def print_citations(interaction) -> None:
    """Print URL citations when the Gemini response contains them."""
    citations = []
    for step in getattr(interaction, "steps", []) or []:
        for block in getattr(step, "content", []) or []:
            for annotation in getattr(block, "annotations", []) or []:
                if getattr(annotation, "type", None) == "url_citation":
                    url = getattr(annotation, "url", None)
                    title = getattr(annotation, "title", None)
                    if url and (title, url) not in citations:
                        citations.append((title or "Source", url))

    if citations:
        print("\nSources:")
        for index, (title, url) in enumerate(citations, start=1):
            print(f"  [{index}] {title} — {url}")


def create_interaction(client: genai.Client, prompt: str, previous_id: Optional[str], use_search: bool):
    """Send one turn, optionally chained to the previous interaction."""
    kwargs = {
        "model": MODEL,
        "input": prompt,
        "tools": [{"type": "google_search"}] if use_search else [],
    }
    if previous_id:
        kwargs["previous_interaction_id"] = previous_id
    return client.interactions.create(**kwargs)


def main() -> None:
    try:
        client = build_client()
    except RuntimeError as exc:
        print(f"Configuration error: {exc}")
        sys.exit(1)

    previous_id = None
    use_search = True

    print("=" * 58)
    print("Gemini Search Assistant")
    print(f"Model: {MODEL}")
    print(f"Google Search grounding: {'ON' if use_search else 'OFF'}")
    print("Type /help for commands.")
    print("=" * 58)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return

        if not user_input:
            continue

        if user_input.lower() == "/exit":
            print("Goodbye!")
            return

        if user_input.lower() == "/help":
            print("/search on   Enable Google Search grounding")
            print("/search off  Disable Google Search grounding")
            print("/reset       Start a new conversation")
            print("/help        Show commands")
            print("/exit        Exit")
            continue

        if user_input.lower() == "/reset":
            previous_id = None
            print("Conversation reset.")
            continue

        if user_input.lower() == "/search on":
            use_search = True
            print("Google Search grounding enabled.")
            continue

        if user_input.lower() == "/search off":
            use_search = False
            print("Google Search grounding disabled.")
            continue

        try:
            interaction = create_interaction(
                client=client,
                prompt=user_input,
                previous_id=previous_id,
                use_search=use_search,
            )
            previous_id = interaction.id
            print(f"\nAssistant: {interaction.output_text}")
            print_citations(interaction)
        except Exception as exc:  # User-facing CLI: show a readable error and continue.
            print(f"\nRequest failed: {exc}")


if __name__ == "__main__":
    main()
