"""
Interactive CLI για το Academic Assistant.
Τρέχει το LangGraph σε loop, δέχεται queries από τον χρήστη.

Usage:
    python chat.py

Commands:
    exit, quit, q  - τερματισμός
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.graph import run_agent


def print_banner():
    print("=" * 70)
    print("  ACADEMIC ASSISTANT — Basketball Analytics")
    print("  Type your question and press Enter")
    print("  Commands: exit, quit, q to terminate")
    print("=" * 70)


def print_separator():
    print("\n" + "─" * 70 + "\n")


def main():
    print_banner()
    
    while True:
        print_separator()
        try:
            query = input("Your question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nGoodbye!")
            break
        
        # Empty input → skip
        if not query:
            continue
        
        # Exit commands
        if query.lower() in {"exit", "quit", "q"}:
            print("\nGoodbye!")
            break
        
        print()
        try:
            result = run_agent(query)
            
            print("\n" + "=" * 70)
            print("ANSWER:")
            print("=" * 70)
            print(result["answer"])
            
        except KeyboardInterrupt:
            print("\n\n[Interrupted by user]")
            continue
        except Exception as e:
            print(f"\n[ERROR] {e}")
            continue


if __name__ == "__main__":
    main()