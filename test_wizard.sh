#!/bin/bash
#
# Simple test script to verify Simple Wizard is working
#
# Usage:
#   1. In terminal 1: simple-wizard
#   2. In terminal 2: ./test_wizard.sh

SOCKET="/tmp/simple-wizard.sock"

echo "Testing Simple Wizard..."
echo "Make sure simple-wizard is running in another terminal!"
echo ""

# Check if socket exists
if [ ! -S "$SOCKET" ]; then
    echo "ERROR: Wizard socket not found at $SOCKET"
    echo "Please start the wizard first with: simple-wizard"
    exit 1
fi

echo "Socket found. Running tests..."
echo ""

# Test 1: Set info
echo "Test 1: Setting wizard info..."
simple-wizard-client --socket "$SOCKET" set-info \
    --title "Test Wizard" \
    --description "Testing Simple Wizard functionality" \
    --help-text "This is a test run."

# Test 2: Progress
echo "Test 2: Setting progress..."
simple-wizard-client --socket "$SOCKET" set-progress --total 3 --current 1 --status "Test in progress"

# Test 3: Welcome page
echo "Test 3: Showing welcome page (click Next in wizard)..."
simple-wizard-client --socket "$SOCKET" welcome \
    --title "Welcome to Tests" \
    --message "This is a test of the welcome page. Click Next to continue."

# Test 4: Question
echo "Test 4: Showing question (select an option in wizard)..."
simple-wizard-client --socket "$SOCKET" set-progress --current 2
response=$(simple-wizard-client --socket "$SOCKET" question \
    --title "Test Question" \
    --message "Which option do you prefer?" \
    --buttons "Option A" "Option B" "Option C")

selected=$(echo "$response" | jq -r '.response.button // empty')
echo "You selected: $selected"

# Test 5: Complete
echo "Test 5: Showing completion page..."
simple-wizard-client --socket "$SOCKET" set-progress --current 3 --status "Tests complete"
simple-wizard-client --socket "$SOCKET" complete \
    --title "Tests Complete" \
    --message "All tests passed successfully!"

echo ""
echo "Tests completed! The wizard should still be running."
echo "Run 'simple-wizard-client quit' to close it."
