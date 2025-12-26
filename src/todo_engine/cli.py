"""
Command-line interface for the Core Todo Engine
"""
import argparse
import json
import sys
from typing import Optional
from .models import Task, create_task, update_task, toggle_task_completion
from .storage import storage
from .logger import setup_logger, log_user_action, log_error


class TodoCLI:
    """
    Command-line interface for the Todo Engine.
    """
    def __init__(self):
        self.logger = setup_logger()
        self.parser = self._create_parser()

    def _validate_title(self, title: str) -> str:
        """
        Validate the title parameter.

        Args:
            title: The title to validate

        Returns:
            str: The validated title

        Raises:
            argparse.ArgumentTypeError: If the title is invalid
        """
        if not title or len(title) == 0:
            raise argparse.ArgumentTypeError("Title cannot be empty")
        if len(title) > 255:
            raise argparse.ArgumentTypeError("Title cannot exceed 255 characters")
        return title

    def _validate_description(self, description: str) -> str:
        """
        Validate the description parameter.

        Args:
            description: The description to validate

        Returns:
            str: The validated description

        Raises:
            argparse.ArgumentTypeError: If the description is invalid
        """
        if len(description) > 1000:
            raise argparse.ArgumentTypeError("Description cannot exceed 1000 characters")
        return description

    def _create_parser(self) -> argparse.ArgumentParser:
        """
        Create the argument parser with all available commands.

        Returns:
            argparse.ArgumentParser: Configured argument parser
        """
        parser = argparse.ArgumentParser(
            prog="todo",
            description="Core Todo Engine - Manage your tasks from the command line",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  Add a task:           todo add --title "Buy groceries" --description "Milk, bread, eggs"
  List tasks:           todo list
  Update a task:        todo update --id <task-id> --title "New title"
  Delete a task:        todo delete --id <task-id>
  Mark complete:        todo complete --id <task-id>
            """
        )

        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # Add command
        add_parser = subparsers.add_parser("add", help="Add a new task")
        add_parser.add_argument("--title", required=True, type=self._validate_title,
                               help="Task title (1-255 characters)")
        add_parser.add_argument("--description", required=False, default="",
                               help="Task description (0-1000 characters)")

        # List command
        list_parser = subparsers.add_parser("list", help="List all tasks")

        # Update command
        update_parser = subparsers.add_parser("update", help="Update an existing task")
        update_parser.add_argument("--id", required=True, help="Task ID to update")
        update_parser.add_argument("--title", required=False, type=self._validate_title,
                                  help="New task title (1-255 characters)")
        update_parser.add_argument("--description", required=False, type=self._validate_description,
                                  help="New task description (0-1000 characters)")

        # Delete command
        delete_parser = subparsers.add_parser("delete", help="Delete a task")
        delete_parser.add_argument("--id", required=True, help="Task ID to delete")

        # Complete command
        complete_parser = subparsers.add_parser("complete", help="Toggle task completion status")
        complete_parser.add_argument("--id", required=True, help="Task ID to toggle")

        # AI command - to access the conversational interface from CLI
        ai_parser = subparsers.add_parser("ai", help="Start the AI conversational interface")
        ai_parser.add_argument("--prompt", required=False, help="Direct prompt to AI assistant (optional)")

        return parser

    def run(self, args: Optional[list] = None):
        """
        Run the CLI with the given arguments.
        
        Args:
            args: List of arguments to parse (default: sys.argv[1:])
        """
        if args is None:
            args = sys.argv[1:]

        try:
            parsed_args = self.parser.parse_args(args)

            if not parsed_args.command:
                self.parser.print_help()
                return

            # Log the user action
            log_user_action(self.logger, parsed_args.command, str(vars(parsed_args)))

            # Execute the appropriate command
            if parsed_args.command == "add":
                self._add_task(parsed_args)
            elif parsed_args.command == "list":
                self._list_tasks()
            elif parsed_args.command == "update":
                self._update_task(parsed_args)
            elif parsed_args.command == "delete":
                self._delete_task(parsed_args)
            elif parsed_args.command == "complete":
                self._complete_task(parsed_args)
            elif parsed_args.command == "ai":
                self._ai_interface(parsed_args)
        except SystemExit:
            # argparse calls sys.exit() when help is displayed or there's an error
            pass
        except Exception as e:
            log_error(self.logger, e, f"command: {parsed_args.command if 'parsed_args' in locals() else 'unknown'}")
            print(f"Error: {str(e)}", file=sys.stderr)
            sys.exit(1)

    def _add_task(self, args):
        """
        Handle the add command.

        Args:
            args: Parsed arguments
        """
        try:
            task = create_task(args.title, args.description)
            storage.add_task(task)
            # Only output the JSON result, not logs
            print(json.dumps(task.__dict__, indent=2))
        except ValueError as e:
            error_response = {
                "error_code": "INVALID_TITLE",
                "message": str(e)
            }
            print(json.dumps(error_response, indent=2))
            sys.exit(11)  # Exit code 11 for invalid title
        except Exception as e:
            if "PERSISTENCE_WRITE_FAILED" in str(e):
                error_response = {
                    "error_code": "PERSISTENCE_WRITE_FAILED",
                    "message": str(e)
                }
            else:
                error_response = {
                    "error_code": "UNKNOWN_ERROR",
                    "message": f"Error creating task: {str(e)}"
                }
            print(json.dumps(error_response, indent=2))
            sys.exit(1)

    def _list_tasks(self, args=None):
        """
        Handle the list command.
        
        Args:
            args: Parsed arguments (not used for this command)
        """
        tasks = storage.get_all_tasks()
        print(json.dumps([task.__dict__ for task in tasks], indent=2))

    def _update_task(self, args):
        """
        Handle the update command.

        Args:
            args: Parsed arguments
        """
        task = storage.get_task(args.id)
        if not task:
            error_response = {
                "error_code": "TASK_NOT_FOUND",
                "message": f"Task with ID {args.id} does not exist"
            }
            print(json.dumps(error_response, indent=2))
            sys.exit(10)  # Exit code 10 for task not found

        try:
            # Determine which fields to update
            title = args.title if hasattr(args, 'title') and args.title is not None else None
            description = args.description if hasattr(args, 'description') and args.description is not None else None

            updated_task = update_task(task, title, description)
            storage.update_task(args.id, updated_task)
            print(json.dumps(updated_task.__dict__, indent=2))
        except ValueError as e:
            error_response = {
                "error_code": "INVALID_TITLE",
                "message": str(e)
            }
            print(json.dumps(error_response, indent=2))
            sys.exit(11)  # Exit code 11 for invalid title
        except Exception as e:
            if "PERSISTENCE_WRITE_FAILED" in str(e):
                error_response = {
                    "error_code": "PERSISTENCE_WRITE_FAILED",
                    "message": str(e)
                }
            else:
                error_response = {
                    "error_code": "UNKNOWN_ERROR",
                    "message": f"Error updating task: {str(e)}"
                }
            print(json.dumps(error_response, indent=2))
            sys.exit(1)

    def _delete_task(self, args):
        """
        Handle the delete command.
        
        Args:
            args: Parsed arguments
        """
        try:
            success = storage.delete_task(args.id)
            if not success:
                error_response = {
                    "error_code": "TASK_NOT_FOUND",
                    "message": f"Task with ID {args.id} does not exist"
                }
                print(json.dumps(error_response, indent=2))
                sys.exit(10)  # Exit code 10 for task not found

            print(json.dumps({
                "message": "Task deleted successfully",
                "deleted_task_id": args.id
            }, indent=2))
        except Exception as e:
            if "PERSISTENCE_WRITE_FAILED" in str(e):
                error_response = {
                    "error_code": "PERSISTENCE_WRITE_FAILED",
                    "message": str(e)
                }
            else:
                error_response = {
                    "error_code": "UNKNOWN_ERROR",
                    "message": f"Error deleting task: {str(e)}"
                }
            print(json.dumps(error_response, indent=2))
            sys.exit(1)

    def _complete_task(self, args):
        """
        Handle the complete command.
        
        Args:
            args: Parsed arguments
        """
        task = storage.get_task(args.id)
        if not task:
            error_response = {
                "error_code": "TASK_NOT_FOUND",
                "message": f"Task with ID {args.id} does not exist"
            }
            print(json.dumps(error_response, indent=2))
            sys.exit(10)  # Exit code 10 for task not found

        updated_task = toggle_task_completion(task)
        try:
            storage.update_task(args.id, updated_task)
            print(json.dumps(updated_task.__dict__, indent=2))
        except Exception as e:
            if "PERSISTENCE_WRITE_FAILED" in str(e):
                error_response = {
                    "error_code": "PERSISTENCE_WRITE_FAILED",
                    "message": str(e)
                }
            else:
                error_response = {
                    "error_code": "UNKNOWN_ERROR",
                    "message": f"Error updating task completion: {str(e)}"
                }
            print(json.dumps(error_response, indent=2))
            sys.exit(1)

    def _ai_interface(self, args):
        """
        Handle the AI interface command.

        Args:
            args: Parsed arguments
        """
        if args.prompt:
            # If a direct prompt is provided, process it and return
            from .ai_assistant import ai_assistant
            result = ai_assistant.process_command(args.prompt)

            if result["status"] == "success":
                print(result["data"]["message"])
            else:
                print(f"Error: {result['error']['message']}")
        else:
            # Otherwise, start the interactive AI interface
            from ..main import start_conversational_interface
            start_conversational_interface()


def main():
    """
    Main entry point for the CLI.
    """
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()