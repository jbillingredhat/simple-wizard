#!/usr/bin/env python3
"""
Client for controlling the wizard from bash scripts.
"""

import socket
import json
import sys
import argparse


class WizardClient:
    """Client for communicating with the wizard."""

    def __init__(self, socket_path="/tmp/simple-wizard.sock"):
        self.socket_path = socket_path

    def _send_command(self, command):
        """Send a command to the wizard and return the response."""
        try:
            client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            client.connect(self.socket_path)
            client.sendall(json.dumps(command).encode('utf-8') + b"\n")

            # Receive response
            data = b""
            while True:
                chunk = client.recv(4096)
                if not chunk:
                    break
                data += chunk
                if b"\n" in data:
                    break

            client.close()

            if data:
                return json.loads(data.decode('utf-8'))
            return None

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def set_info(self, title=None, description=None, help_text=None):
        """Update the wizard information panel."""
        command = {"command": "set_info"}
        if title:
            command["title"] = title
        if description:
            command["description"] = description
        if help_text:
            command["help_text"] = help_text
        return self._send_command(command)

    def set_progress(self, current=None, total=None, status=None):
        """Update the progress bar."""
        command = {"command": "set_progress"}
        if current is not None:
            command["current"] = current
        if total is not None:
            command["total"] = total
        if status:
            command["status"] = status
        return self._send_command(command)

    def show_welcome(self, title="Welcome", message="", **kwargs):
        """Show welcome page."""
        command = {
            "command": "show_page",
            "page_type": "welcome",
            "params": {
                "title": title,
                "message": message,
                **kwargs
            }
        }
        return self._send_command(command)

    def show_file(self, title="Select File", message="", default_path="", **kwargs):
        """Show file selection page."""
        command = {
            "command": "show_page",
            "page_type": "file",
            "params": {
                "title": title,
                "message": message,
                "default_path": default_path,
                **kwargs
            }
        }
        return self._send_command(command)

    def show_directory(self, title="Select Directory", message="", default_path="", **kwargs):
        """Show directory selection page."""
        command = {
            "command": "show_page",
            "page_type": "directory",
            "params": {
                "title": title,
                "message": message,
                "default_path": default_path,
                **kwargs
            }
        }
        return self._send_command(command)

    def show_password(self, title="Enter Password", message="", confirm=True, **kwargs):
        """Show password entry page."""
        command = {
            "command": "show_page",
            "page_type": "password",
            "params": {
                "title": title,
                "message": message,
                "confirm": confirm,
                **kwargs
            }
        }
        return self._send_command(command)

    def show_question(self, title="Question", message="", buttons=None, **kwargs):
        """Show question page with buttons."""
        if buttons is None:
            buttons = ["Yes", "No"]
        command = {
            "command": "show_page",
            "page_type": "question",
            "params": {
                "title": title,
                "message": message,
                "buttons": buttons,
                **kwargs
            }
        }
        return self._send_command(command)

    def show_text(self, title="Enter Text", message="", default_text="", placeholder="",
                  validate=None, validation_message=None, **kwargs):
        """Show text entry page with optional validation.

        Args:
            validate: Either a preset name ('email', 'url', 'ipv4', 'port', 'hostname',
                     'username', 'number', 'positive_number', 'alphanumeric') or a custom regex
            validation_message: Custom error message (uses preset message if not provided)
        """
        command = {
            "command": "show_page",
            "page_type": "text",
            "params": {
                "title": title,
                "message": message,
                "default_text": default_text,
                "placeholder": placeholder,
                **kwargs
            }
        }
        if validate:
            command["params"]["validate"] = validate
        if validation_message:
            command["params"]["validation_message"] = validation_message
        return self._send_command(command)

    def show_warning(self, title="Warning", message="", **kwargs):
        """Show warning page."""
        command = {
            "command": "show_page",
            "page_type": "warning",
            "params": {
                "title": title,
                "message": message,
                **kwargs
            }
        }
        return self._send_command(command)

    def show_error(self, title="Error", message="", **kwargs):
        """Show error page."""
        command = {
            "command": "show_page",
            "page_type": "error",
            "params": {
                "title": title,
                "message": message,
                **kwargs
            }
        }
        return self._send_command(command)

    def show_complete(self, title="Complete", message="Installation completed successfully!", **kwargs):
        """Show completion page."""
        command = {
            "command": "show_page",
            "page_type": "complete",
            "params": {
                "title": title,
                "message": message,
                **kwargs
            }
        }
        return self._send_command(command)

    def append_log(self, message):
        """Append a message to the log panel."""
        command = {"command": "append_log", "message": message}
        return self._send_command(command)

    def clear_log(self):
        """Clear the log panel."""
        command = {"command": "clear_log"}
        return self._send_command(command)

    def quit(self):
        """Tell the wizard to quit."""
        command = {"command": "quit"}
        return self._send_command(command)


def main():
    """Command-line interface for the client."""
    parser = argparse.ArgumentParser(description="Simple Wizard Client")
    parser.add_argument("--socket", default="/tmp/simple-wizard.sock",
                       help="Unix socket path for IPC")

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # set-info command
    info_parser = subparsers.add_parser("set-info", help="Set wizard information")
    info_parser.add_argument("--title", help="Title text")
    info_parser.add_argument("--description", help="Description text")
    info_parser.add_argument("--help-text", help="Help text")

    # set-progress command
    progress_parser = subparsers.add_parser("set-progress", help="Set progress")
    progress_parser.add_argument("--current", type=int, help="Current step")
    progress_parser.add_argument("--total", type=int, help="Total steps")
    progress_parser.add_argument("--status", help="Status text")

    # welcome command
    welcome_parser = subparsers.add_parser("welcome", help="Show welcome page")
    welcome_parser.add_argument("--title", default="Welcome", help="Title")
    welcome_parser.add_argument("--message", default="", help="Message")

    # file command
    file_parser = subparsers.add_parser("file", help="Show file selection page")
    file_parser.add_argument("--title", default="Select File", help="Title")
    file_parser.add_argument("--message", default="", help="Message")
    file_parser.add_argument("--default", default="", help="Default path")

    # directory command
    dir_parser = subparsers.add_parser("directory", help="Show directory selection page")
    dir_parser.add_argument("--title", default="Select Directory", help="Title")
    dir_parser.add_argument("--message", default="", help="Message")
    dir_parser.add_argument("--default", default="", help="Default path")

    # password command
    pass_parser = subparsers.add_parser("password", help="Show password entry page")
    pass_parser.add_argument("--title", default="Enter Password", help="Title")
    pass_parser.add_argument("--message", default="", help="Message")
    pass_parser.add_argument("--no-confirm", action="store_true", help="Don't ask for confirmation")

    # question command
    question_parser = subparsers.add_parser("question", help="Show question page")
    question_parser.add_argument("--title", default="Question", help="Title")
    question_parser.add_argument("--message", required=True, help="Question message")
    question_parser.add_argument("--buttons", nargs="+", default=["Yes", "No"], help="Button labels")

    # text command
    text_parser = subparsers.add_parser("text", help="Show text entry page")
    text_parser.add_argument("--title", default="Enter Text", help="Title")
    text_parser.add_argument("--message", default="", help="Message")
    text_parser.add_argument("--default", default="", help="Default text")
    text_parser.add_argument("--placeholder", default="", help="Placeholder text")
    text_parser.add_argument("--validate", help="Validation preset (email, url, ipv4, port, hostname, username, number, positive_number, alphanumeric) or custom regex")
    text_parser.add_argument("--validation-message", help="Custom validation error message")

    # warning command
    warning_parser = subparsers.add_parser("warning", help="Show warning page")
    warning_parser.add_argument("--title", default="Warning", help="Title")
    warning_parser.add_argument("--message", required=True, help="Warning message")

    # error command
    error_parser = subparsers.add_parser("error", help="Show error page")
    error_parser.add_argument("--title", default="Error", help="Title")
    error_parser.add_argument("--message", required=True, help="Error message")

    # complete command
    complete_parser = subparsers.add_parser("complete", help="Show completion page")
    complete_parser.add_argument("--title", default="Complete", help="Title")
    complete_parser.add_argument("--message", default="Installation completed successfully!", help="Message")

    # log command
    log_parser = subparsers.add_parser("log", help="Append message to log")
    log_parser.add_argument("--message", required=True, help="Log message")

    # clear-log command
    subparsers.add_parser("clear-log", help="Clear the log")

    # quit command
    subparsers.add_parser("quit", help="Quit the wizard")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    client = WizardClient(socket_path=args.socket)

    # Execute command
    result = None
    if args.command == "set-info":
        result = client.set_info(args.title, args.description, args.help_text)
    elif args.command == "set-progress":
        result = client.set_progress(args.current, args.total, args.status)
    elif args.command == "welcome":
        result = client.show_welcome(args.title, args.message)
    elif args.command == "file":
        result = client.show_file(args.title, args.message, args.default)
    elif args.command == "directory":
        result = client.show_directory(args.title, args.message, args.default)
    elif args.command == "password":
        result = client.show_password(args.title, args.message, not args.no_confirm)
    elif args.command == "question":
        result = client.show_question(args.title, args.message, args.buttons)
    elif args.command == "text":
        result = client.show_text(args.title, args.message, args.default, args.placeholder,
                                  args.validate, args.validation_message)
    elif args.command == "warning":
        result = client.show_warning(args.title, args.message)
    elif args.command == "error":
        result = client.show_error(args.title, args.message)
    elif args.command == "complete":
        result = client.show_complete(args.title, args.message)
    elif args.command == "log":
        result = client.append_log(args.message)
    elif args.command == "clear-log":
        result = client.clear_log()
    elif args.command == "quit":
        result = client.quit()

    # Print result
    if result:
        print(json.dumps(result, indent=2))
        if result.get("status") == "error":
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
