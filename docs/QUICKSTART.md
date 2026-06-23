# Simple Wizard Quick Start

## Installation

```bash
# Install dependencies (Fedora)
sudo dnf install python3-gobject gtk4

# Install Simple Wizard
pip install -e .
```

## Basic Usage

### Terminal 1: Start the Wizard

```bash
simple-wizard
```

### Terminal 2: Control the Wizard

```bash
# Welcome screen
simple-wizard-client welcome --title "Hello" --message "Welcome to the installer!"

# Ask for directory
simple-wizard-client directory --title "Install Location" --default "$HOME/myapp"

# Ask a question
simple-wizard-client question --message "Install desktop icon?" --buttons "Yes" "No"

# Show completion
simple-wizard-client complete --message "Done!"

# Quit
simple-wizard-client quit
```

## Example Script

```bash
#!/bin/bash

# Set up wizard
simple-wizard-client set-info --title "My App" --description "Installer v1.0"
simple-wizard-client set-progress --total 3

# Step 1: Welcome
simple-wizard-client set-progress --current 1 --status "Welcome"
simple-wizard-client welcome --title "Welcome" --message "Let's install My App!"

# Step 2: Get install directory
simple-wizard-client set-progress --current 2 --status "Configuration"
response=$(simple-wizard-client directory --title "Install Location")
install_dir=$(echo "$response" | jq -r '.response.path')

# Step 3: Complete
simple-wizard-client set-progress --current 3 --status "Complete"
simple-wizard-client complete --message "Installed to $install_dir"

simple-wizard-client quit
```

## Testing

Run the included test script:

```bash
# Terminal 1
simple-wizard

# Terminal 2
./test_wizard.sh
```

## Page Types

- `welcome` - Welcome message with Next button
- `file` - File selection dialog
- `directory` - Directory selection dialog
- `password` - Password entry (with optional confirmation)
- `question` - Multiple choice buttons
- `text` - Free text input
- `warning` - Warning message
- `error` - Error message
- `complete` - Completion message

## Examples

See `examples/` directory for:
- `example_install.sh` - Bash script example
- `example_install.py` - Python script example

## Documentation

- `README.md` - Project overview
- `USAGE.md` - Detailed usage documentation
- `QUICKSTART.md` - This file
