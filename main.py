#!/usr/bin/env python3
"""
Core Todo Engine - Phase III
Entry point for the command-line interface application with conversational AI
"""
import sys
from src.todo_engine.cli import main as cli_main
from src.todo_engine.ai_assistant import ai_assistant


def main():
    """
    Main entry point for the application supporting both CLI and AI interfaces.
    """
    if len(sys.argv) > 1:
        # If command line arguments are provided, use traditional CLI
        cli_main()
    else:
        # If no arguments, start conversational AI interface
        start_conversational_interface()


def start_conversational_interface():
    """
    Start the conversational AI interface.
    """
    print("Welcome to the Todo AI Assistant!")
    print("You can manage your tasks using natural language.")
    print("Type 'quit' or 'exit' to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Goodbye! Have a productive day!")
                break

            if not user_input:
                continue

            # Process the command with the AI assistant
            from src.todo_engine.ai_assistant import ai_assistant
            result = ai_assistant.process_command(user_input)

            # Format and print the response (avoiding emoji encoding issues)
            if result["status"] == "success":
                message = result["data"]["message"]
                # Remove or replace emojis to avoid encoding issues on some terminals
                message = message.replace("✅", "[COMPLETED]").replace("❌", "[ERROR]").replace("📋", "[TASKS]")
                print(f"AI: {message}\n")
            else:
                error_msg = result["error"]["message"]
                # Remove or replace emojis to avoid encoding issues on some terminals
                error_msg = error_msg.replace("✅", "[COMPLETED]").replace("❌", "[ERROR]").replace("📋", "[TASKS]")
                print(f"AI: {error_msg}\n")

        except KeyboardInterrupt:
            print("\nGoodbye! Have a productive day!")
            break
        except Exception as e:
            print(f"Sorry, I encountered an error: {str(e)}\n")


if __name__ == "__main__":
    main()