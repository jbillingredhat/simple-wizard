# Simple Wizard Usage Guide

## Overview

Simple Wizard is a scriptable GTK4-based installation wizard for Linux. It consists of two components:

1. **Wizard Server** (`simple-wizard`) - The GTK4 GUI application
2. **Wizard Client** (`simple-wizard-client`) - Command-line tool for controlling the wizard

## Installation

### System Requirements

- Fedora Linux (or other Linux with GTK4)
- Python 3.8 or higher
- GTK4
- PyGObject

### Install Dependencies

```bash
sudo dnf install python3-gobject gtk4
```

### Install Simple Wizard

```bash
cd /path/to/simple-wizard
pip install -e .
```

## Quick Start

### 1. Start the Wizard

In one terminal, start the wizard server:

```bash
simple-wizard
```

The wizard window will appear and wait for commands.

### 2. Control from Script

In another terminal (or from your installation script), use the client:

```bash
# Show a welcome page
simple-wizard-client welcome --title "Welcome" --message "Hello, World!"

# Ask for an installation directory
simple-wizard-client directory --title "Install Location" --default "$HOME/myapp"

# Show completion
simple-wizard-client complete --message "Installation finished!"

# Quit the wizard
simple-wizard-client quit
```

## Client Commands

### Set Information Panel

Update the left sidebar with application information:

```bash
simple-wizard-client set-info \
    --title "My Application" \
    --description "Version 1.0 Installer" \
    --help-text "This wizard will install My Application."
```

### Set Progress

Update the progress bar:

```bash
# Set total steps (hides progress bar if total is 0)
simple-wizard-client set-progress --total 5

# Update current step and status
simple-wizard-client set-progress --current 3 --status "Installing files..."
```

### Welcome Page

Show a welcome page with informational text:

```bash
simple-wizard-client welcome \
    --title "Welcome to My App" \
    --message "This wizard will guide you through installation."
```

Returns: `{"action": "next"}`

### File Selection

Prompt user to select a file:

```bash
simple-wizard-client file \
    --title "Select Configuration File" \
    --message "Choose a config file to import" \
    --default "/etc/myapp/config.ini"
```

Returns: `{"action": "next", "path": "/selected/file/path"}` or `{"action": "cancel"}`

### Directory Selection

Prompt user to select a directory:

```bash
simple-wizard-client directory \
    --title "Installation Directory" \
    --message "Where should we install the application?" \
    --default "$HOME/myapp"
```

Returns: `{"action": "next", "path": "/selected/directory"}` or `{"action": "cancel"}`

### Password Entry

Prompt for password entry:

```bash
# With confirmation
simple-wizard-client password \
    --title "Set Password" \
    --message "Create an admin password"

# Without confirmation
simple-wizard-client password \
    --title "Enter Password" \
    --no-confirm
```

Returns: `{"action": "next", "password": "entered_password"}` or `{"action": "cancel"}`

### Question with Buttons

Ask a question with custom buttons:

```bash
simple-wizard-client question \
    --title "Installation Type" \
    --message "What type of installation?" \
    --buttons "Full" "Minimal" "Custom"
```

Returns: `{"action": "button", "button": "Full"}` (or whichever button was clicked)

### Text Entry

Simple text input with optional validation:

```bash
# Without validation
simple-wizard-client text \
    --title "User Information" \
    --message "Enter your name" \
    --placeholder "John Doe"

# With email validation (preset)
simple-wizard-client text \
    --title "Email Address" \
    --message "Enter your email address" \
    --placeholder "user@example.com" \
    --validate "email"

# With custom regex validation
simple-wizard-client text \
    --title "Product Code" \
    --message "Enter product code (ABC-1234)" \
    --validate "^[A-Z]{3}-[0-9]{4}$" \
    --validation-message "Format must be ABC-1234"
```

**Available validation presets:**
- `email` - Valid email address
- `url` - Valid HTTP/HTTPS URL
- `ipv4` - Valid IPv4 address
- `port` - Valid port number (1-65535)
- `hostname` - Valid hostname
- `username` - Alphanumeric username (3-32 chars)
- `number` - Any integer
- `positive_number` - Positive integer
- `alphanumeric` - Letters and numbers only

Returns: `{"action": "next", "text": "entered_text"}` or `{"action": "cancel"}`

If validation fails, an error message is displayed and the user must correct the input.

### Warning

Show a warning message:

```bash
simple-wizard-client warning \
    --title "Important Notice" \
    --message "This will modify system files. Continue?"
```

Returns: `{"action": "ok"}`

### Error

Show an error message:

```bash
simple-wizard-client error \
    --title "Installation Failed" \
    --message "Could not write to directory. Check permissions."
```

Returns: `{"action": "ok"}`

### Complete

Show completion page:

```bash
simple-wizard-client complete \
    --title "Success!" \
    --message "Installation completed successfully."
```

Returns: `{"action": "finish"}`

### Log Messages

Append a message to the expandable log panel:

```bash
simple-wizard-client log --message "Installing packages..."
```

The log panel appears at the bottom of the window and can be expanded/collapsed by clicking the triangle icon next to "Installation Log".

### Clear Log

Clear all messages from the log panel:

```bash
simple-wizard-client clear-log
```

### Quit

Close the wizard:

```bash
simple-wizard-client quit
```

## Using from Bash Scripts

The client outputs JSON responses. Here's how to parse them using `jq`:

```bash
#!/bin/bash

# Call the wizard and capture output
response=$(simple-wizard-client directory --title "Select Directory")

# Extract the path using jq
install_dir=$(echo "$response" | jq -r '.response.path // empty')

echo "Selected: $install_dir"

# Check if user cancelled
action=$(echo "$response" | jq -r '.response.action // empty')

if [ "$action" == "cancel" ]; then
    echo "User cancelled"
    exit 1
fi
```

**Note:** Requires `jq` to be installed: `sudo dnf install jq`

See `examples/example_install.sh` for a complete example.

## Using from Python

You can also use the Python API directly:

```python
from simple_wizard.client import WizardClient

client = WizardClient()

# Set wizard info
client.set_info(
    title="My App Installer",
    description="Version 1.0",
    help_text="Follow the steps to install."
)

# Show welcome page
response = client.show_welcome(
    title="Welcome",
    message="Let's get started!"
)

# Get directory
response = client.show_directory(
    title="Install Location",
    default_path="/opt/myapp"
)

install_dir = response.get('response', {}).get('path')
print(f"Installing to: {install_dir}")

# Complete
client.show_complete(message="Installation finished!")
client.quit()
```

See `examples/example_install.py` for a complete example.

## Custom Socket Path

Both the wizard and client support custom socket paths:

```bash
# Start wizard with custom socket
simple-wizard --socket /tmp/my-installer.sock

# Use client with custom socket
simple-wizard-client --socket /tmp/my-installer.sock welcome --title "Hello"
```

## Tips

1. **Progress Tracking**: Set the total number of steps at the start, then update current step as you go
2. **Error Handling**: Always check return status and handle cancellations
3. **Help Text**: Use the info panel's help text to provide context-sensitive help
4. **Status Updates**: Update the status text at the bottom to show what's happening
5. **Validation**: The wizard validates password confirmation automatically

## Architecture

- **IPC**: Unix domain sockets for client-server communication
- **Threading**: Server runs in background thread, GTK main loop in main thread
- **Response Model**: Synchronous - client waits for user interaction
- **Page Management**: Each page type is a separate class in `pages.py`

## Troubleshooting

**Socket already in use**
```bash
rm /tmp/simple-wizard.sock
```

**GTK4 not found**
```bash
sudo dnf install gtk4 python3-gobject
```

**Client can't connect**
- Make sure the wizard is running
- Check socket path matches between wizard and client
- Verify socket file exists: `ls -l /tmp/simple-wizard.sock`
