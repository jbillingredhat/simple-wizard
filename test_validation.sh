#!/bin/bash
#
# Test script to demonstrate text validation feature
#

SOCKET="/tmp/simple-wizard.sock"

echo "Testing validation feature..."
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
    --title "Validation Demo" \
    --description "Testing input validation" \
    --help-text "Try entering invalid input and see the validation error messages."

simple-wizard-client --socket "$SOCKET" set-progress --total 6

# Test 1: Email validation
echo "Test 1: Email validation..."
simple-wizard-client --socket "$SOCKET" set-progress --current 1 --status "Email validation"
response=$(simple-wizard-client --socket "$SOCKET" text \
    --title "Email Address" \
    --message "Please enter your email address." \
    --placeholder "user@example.com" \
    --validate "email")

email=$(echo "$response" | jq -r '.response.text')
simple-wizard-client --socket "$SOCKET" log --message "Email entered: $email"

# Test 2: URL validation
echo "Test 2: URL validation..."
simple-wizard-client --socket "$SOCKET" set-progress --current 2 --status "URL validation"
response=$(simple-wizard-client --socket "$SOCKET" text \
    --title "Website URL" \
    --message "Enter your website URL." \
    --placeholder "https://example.com" \
    --validate "url")

url=$(echo "$response" | jq -r '.response.text')
simple-wizard-client --socket "$SOCKET" log --message "URL entered: $url"

# Test 3: Port number validation
echo "Test 3: Port number validation..."
simple-wizard-client --socket "$SOCKET" set-progress --current 3 --status "Port validation"
response=$(simple-wizard-client --socket "$SOCKET" text \
    --title "Server Port" \
    --message "Enter the server port number." \
    --placeholder "8080" \
    --validate "port")

port=$(echo "$response" | jq -r '.response.text')
simple-wizard-client --socket "$SOCKET" log --message "Port entered: $port"

# Test 4: Username validation
echo "Test 4: Username validation..."
simple-wizard-client --socket "$SOCKET" set-progress --current 4 --status "Username validation"
response=$(simple-wizard-client --socket "$SOCKET" text \
    --title "Username" \
    --message "Choose a username (3-32 characters, alphanumeric, dashes, underscores)." \
    --placeholder "my_username" \
    --validate "username")

username=$(echo "$response" | jq -r '.response.text')
simple-wizard-client --socket "$SOCKET" log --message "Username entered: $username"

# Test 5: Custom regex validation
echo "Test 5: Custom regex validation..."
simple-wizard-client --socket "$SOCKET" set-progress --current 5 --status "Custom regex"
response=$(simple-wizard-client --socket "$SOCKET" text \
    --title "Product Code" \
    --message "Enter a product code (format: ABC-1234)." \
    --placeholder "ABC-1234" \
    --validate "^[A-Z]{3}-[0-9]{4}$" \
    --validation-message "Product code must be 3 uppercase letters, a dash, and 4 digits (e.g., ABC-1234)")

product_code=$(echo "$response" | jq -r '.response.text')
simple-wizard-client --socket "$SOCKET" log --message "Product code entered: $product_code"

# Complete
simple-wizard-client --socket "$SOCKET" set-progress --current 6 --status "Complete"
response=$(simple-wizard-client --socket "$SOCKET" complete \
    --title "Validation Tests Complete!" \
    --message "All validation tests passed!

Email: $email
URL: $url
Port: $port
Username: $username
Product Code: $product_code

All inputs were validated successfully.")

echo ""
echo "Validation demo completed!"
echo "Closing wizard..."
simple-wizard-client --socket "$SOCKET" quit
