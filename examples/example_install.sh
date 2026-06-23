#!/bin/bash
#
# Example installation script using Simple Wizard
#
# This demonstrates how to use the wizard from a bash script.

# Configuration
SOCKET="/tmp/simple-wizard.sock"
CLIENT="simple-wizard-client --socket $SOCKET"

# Helper function to call the client and extract response data
call_wizard() {
    $CLIENT "$@"
}

# Helper function to get response value from JSON
get_response() {
    echo "$1" | jq -r ".response.$2 // empty"
}

echo "Starting installation wizard example..."

# Set up the wizard information
call_wizard set-info \
    --title "Example Application Installer" \
    --description "This wizard will guide you through installing Example App." \
    --help-text "Follow the prompts to complete the installation. You can cancel at any time."

# Set total number of steps
call_wizard set-progress --total 6 --current 0 --status "Starting installation"

# Step 1: Welcome page
call_wizard set-progress --current 1 --status "Welcome"
response=$(call_wizard welcome \
    --title "Welcome to Example App Installer" \
    --message "This wizard will help you install Example App on your system.

Click Next to begin the installation process.")

echo "Welcome response: $response"

# Step 2: Ask for installation directory
call_wizard set-progress --current 2 --status "Selecting installation directory"
response=$(call_wizard directory \
    --title "Installation Directory" \
    --message "Select where you want to install Example App." \
    --default "$HOME/example-app")

INSTALL_DIR=$(get_response "$response" "path")
echo "Selected installation directory: $INSTALL_DIR"

if [ -z "$INSTALL_DIR" ]; then
    call_wizard error --title "Installation Cancelled" --message "No directory selected."
    call_wizard quit
    exit 1
fi

# Step 3: Ask for user's email (with validation)
call_wizard set-progress --current 3 --status "Getting user information"
response=$(call_wizard text \
    --title "User Information" \
    --message "Please enter your email address for registration." \
    --placeholder "user@example.com" \
    --validate "email")

EMAIL=$(get_response "$response" "text")
echo "Email: $EMAIL"

# Step 4: Ask a question
call_wizard set-progress --current 4 --status "Configuration options"
response=$(call_wizard question \
    --title "Desktop Shortcut" \
    --message "Would you like to create a desktop shortcut?" \
    --buttons "Yes" "No" "Ask me later")

SHORTCUT=$(get_response "$response" "button")
echo "Desktop shortcut: $SHORTCUT"

# Step 5: Simulate installation with a warning
call_wizard set-progress --current 5 --status "Installing files"
call_wizard warning \
    --title "Installing Files" \
    --message "The installation will now copy files to your system. This may take a few moments."

# Simulate some work with logging
call_wizard log --message "Starting installation to $INSTALL_DIR"
call_wizard log --message "Creating directory structure..."
sleep 1
call_wizard log --message "Copying application files..."
sleep 1
call_wizard log --message "Setting up configuration..."
call_wizard log --message "Registration email set to: $EMAIL"
call_wizard log --message "Desktop shortcut preference: $SHORTCUT"
sleep 1
call_wizard log --message "Installation complete!"

# Check if something went wrong (for demonstration)
if [ "$EMAIL" == "error@example.com" ]; then
    call_wizard error \
        --title "Installation Failed" \
        --message "An error occurred during installation. Please contact support."
    call_wizard quit
    exit 1
fi

# Step 6: Complete
call_wizard set-progress --current 6 --status "Installation complete"
call_wizard complete \
    --title "Installation Complete!" \
    --message "Example App has been successfully installed to:
$INSTALL_DIR

Your registration email: $EMAIL
Desktop shortcut: $SHORTCUT

Thank you for installing Example App!"

# Quit the wizard
call_wizard quit

echo "Installation script completed."
