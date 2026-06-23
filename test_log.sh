#!/bin/bash
#
# Test script to demonstrate the log panel feature
#

SOCKET="/tmp/simple-wizard.sock"

echo "Testing log panel feature..."
echo "Make sure simple-wizard is running!"
echo ""

# Check if socket exists
if [ ! -S "$SOCKET" ]; then
    echo "ERROR: Wizard socket not found at $SOCKET"
    echo "Please start the wizard first with: simple-wizard"
    exit 1
fi

# Set up the wizard
simple-wizard-client --socket "$SOCKET" set-info \
    --title "Log Panel Demo" \
    --description "Testing the expandable log panel" \
    --help-text "Expand the 'Installation Log' at the bottom to see messages."

simple-wizard-client --socket "$SOCKET" set-progress --total 5

# Show welcome
simple-wizard-client --socket "$SOCKET" set-progress --current 1
simple-wizard-client --socket "$SOCKET" welcome \
    --title "Log Panel Demo" \
    --message "This demo shows the expandable log panel at the bottom of the window.

Expand the 'Installation Log' section to see log messages appear in real-time.

Click Next to continue."

# Simulate a process with logging
simple-wizard-client --socket "$SOCKET" set-progress --current 2 --status "Processing..."

echo "Writing log messages..."
simple-wizard-client --socket "$SOCKET" log --message "Starting process..."
sleep 1
simple-wizard-client --socket "$SOCKET" log --message "Step 1: Initializing..."
sleep 1
simple-wizard-client --socket "$SOCKET" log --message "Step 2: Processing data..."
sleep 1
simple-wizard-client --socket "$SOCKET" log --message "Step 3: Finalizing..."
sleep 1
simple-wizard-client --socket "$SOCKET" log --message "Process complete!"

# Show question
simple-wizard-client --socket "$SOCKET" set-progress --current 3
response=$(simple-wizard-client --socket "$SOCKET" question \
    --title "Clear Log?" \
    --message "Would you like to clear the log?" \
    --buttons "Yes" "No")

choice=$(echo "$response" | jq -r '.response.button')

if [ "$choice" == "Yes" ]; then
    simple-wizard-client --socket "$SOCKET" log --message "Clearing log as requested..."
    sleep 1
    simple-wizard-client --socket "$SOCKET" clear-log
    simple-wizard-client --socket "$SOCKET" log --message "Log cleared!"
else
    simple-wizard-client --socket "$SOCKET" log --message "Keeping existing log entries."
fi

# Complete
simple-wizard-client --socket "$SOCKET" set-progress --current 5 --status "Complete"
response=$(simple-wizard-client --socket "$SOCKET" complete \
    --title "Demo Complete" \
    --message "The log panel demonstration is complete!

You can expand/collapse the log panel using the triangle icon next to 'Installation Log'.

Click Finish to close the wizard.")

echo ""
echo "Demo completed!"
echo "Closing wizard..."
simple-wizard-client --socket "$SOCKET" quit
