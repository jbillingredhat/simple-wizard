# Simple Wizard Features

## Overview

Simple Wizard is a complete solution for creating professional installation wizards on Linux.

## Visual Layout

```
┌────────────────────────────────────────────────────────────────┐
│                     Installation Wizard                        │
├─────────────────────┬──────────────────────────────────────────┤
│                     │                                          │
│    [Icon: 64x64]    │   ┌──────────────────────────────────┐   │
│                     │   │                                  │   │
│  Installation       │   │   Welcome to My Application      │   │
│      Wizard         │   │                                  │   │
│                     │   │   This wizard will guide you     │   │
│  Follow the steps   │   │   through the installation.      │   │
│  to complete the    │   │                                  │   │
│  installation.      │   │   Click Next to continue.        │   │
│                     │   │                                  │   │
│  ─────────────      │   │                                  │   │
│                     │   └──────────────────────────────────┘   │
│  Need help?         │                                          │
│  This wizard will   │                          [Next] ────>    │
│  prompt you for     │                                          │
│  configuration...   │                                          │
│                     │                                          │
├─────────────────────┴──────────────────────────────────────────┤
│  [████████████░░░░░░░░░░░░░░░░░░] 60%                          │
│  Installing files...                                           │
└────────────────────────────────────────────────────────────────┘
```

## Page Types Reference

### 1. Welcome Page
- Large title with welcome message
- Informational text
- Single "Next" button
- Use for: Introduction, license display, important notices

### 2. File Selection
```
Select Configuration File
─────────────────────────
Choose a file to import:

[/path/to/file.conf          ] [Browse...]

                        [Cancel] [Next]
```

### 3. Directory Selection
```
Installation Directory
──────────────────────
Where should we install?

[/home/user/myapp            ] [Browse...]

                        [Cancel] [Next]
```

### 4. Password Entry
```
Set Password
────────────
Create an admin password:

Password:
[••••••••••••••••••••••      ]

Confirm Password:
[••••••••••••••••••••••      ]

                        [Cancel] [Next]
```

### 5. Question with Buttons
```
Installation Type
─────────────────
What type of installation?

                [Full] [Minimal] [Custom]
```

### 6. Text Entry
```
User Information
────────────────
Enter your email address:

[user@example.com            ]

                        [Cancel] [Next]
```

### 7. Warning Page
```
       ⚠️

     Warning

This will modify system files.
Make sure you have backups.

              [OK]
```

### 8. Error Page
```
       ❌

     Error

Installation failed.
Check permissions.

              [OK]
```

### 9. Completion Page
```
       ✓

   Installation Complete!

My App has been successfully
installed to /home/user/myapp

            [Finish]
```

## Client Commands Summary

| Command | Purpose | Returns |
|---------|---------|---------|
| `set-info` | Update sidebar | Status |
| `set-progress` | Update progress bar | Status |
| `welcome` | Show welcome page | `{action: "next"}` |
| `file` | Select file | `{action: "next", path: "..."}` |
| `directory` | Select directory | `{action: "next", path: "..."}` |
| `password` | Enter password | `{action: "next", password: "..."}` |
| `question` | Ask question | `{action: "button", button: "..."}` |
| `text` | Enter text | `{action: "next", text: "..."}` |
| `warning` | Show warning | `{action: "ok"}` |
| `error` | Show error | `{action: "ok"}` |
| `complete` | Show completion | `{action: "finish"}` |
| `quit` | Close wizard | Status |

## Example Workflows

### Simple Installation
```bash
1. welcome     → User clicks Next
2. directory   → User selects /opt/myapp
3. complete    → Installation done
4. quit        → Window closes
```

### Full Installation with Options
```bash
1. welcome           → Introduction
2. set-progress      → Set 6 total steps
3. directory         → Installation location
4. file              → Import config (optional)
5. text              → Email address
6. password          → Admin password
7. question          → Installation type
8. warning           → Ready to install notice
9. [actual install]  → Script does work
10. complete         → Success message
11. quit             → Done
```

### Error Handling Flow
```bash
1. welcome           → Introduction
2. directory         → User selects path
3. [check space]     → Script validates
4. error             → Not enough space!
5. directory         → Try again
6. [check space]     → OK this time
7. complete          → Success
8. quit              → Done
```

## Progress Bar Behavior

### With Total Steps Set
```bash
simple-wizard-client set-progress --total 5

# Shows: [████████████████░░░░░░░░░░░░] 60% (step 3 of 5)
simple-wizard-client set-progress --current 3 --status "Installing..."
```

### Without Total Steps
```bash
# Progress bar hidden, only status text shown
simple-wizard-client set-progress --status "Please wait..."
```

## Info Panel Customization

```bash
# Set title (bold)
simple-wizard-client set-info --title "My Application"

# Set description (under title)
simple-wizard-client set-info --description "Version 2.0 Installer"

# Set help text (bottom of sidebar, context-sensitive)
simple-wizard-client set-info --help-text "
This step asks for your installation directory.
We recommend installing to your home directory.
"
```

## Parsing Responses

### Using jq (Recommended)
```bash
# Get specific field
path=$(echo "$response" | jq -r '.response.path')

# Get with fallback
path=$(echo "$response" | jq -r '.response.path // empty')

# Check action
action=$(echo "$response" | jq -r '.response.action')

# Pretty print for debugging
echo "$response" | jq '.'
```

## Common Patterns

### Validation Loop
```bash
while true; do
    response=$(simple-wizard-client directory --title "Install Location")
    path=$(echo "$response" | jq -r '.response.path')
    
    if [ -w "$path" ]; then
        break  # Path is writable
    fi
    
    simple-wizard-client error \
        --title "Permission Denied" \
        --message "Cannot write to $path. Please choose another location."
done
```

### Conditional Pages
```bash
response=$(simple-wizard-client question \
    --message "Advanced setup?" \
    --buttons "Yes" "No")

choice=$(echo "$response" | jq -r '.response.button')

if [ "$choice" == "Yes" ]; then
    # Show advanced options
    simple-wizard-client text --title "Custom Port" --default "8080"
    # ... more advanced options
fi
```

### Cancel Handling
```bash
response=$(simple-wizard-client directory --title "Select Directory")
action=$(echo "$response" | jq -r '.response.action')

if [ "$action" == "cancel" ]; then
    simple-wizard-client warning \
        --title "Installation Cancelled" \
        --message "Setup was cancelled. No changes were made."
    simple-wizard-client quit
    exit 0
fi
```

## Tips and Best Practices

1. **Always set info panel** - Helps users understand what they're installing
2. **Use progress tracking** - Show users how far along they are
3. **Update status text** - Keep users informed of current action
4. **Validate input** - Check paths, permissions, etc. before proceeding
5. **Handle cancellation** - Always check for cancel action
6. **Use meaningful titles** - Each page should have clear, specific title
7. **Provide help text** - Update sidebar help for each step
8. **Test error paths** - Make sure error handling works
9. **Use appropriate page types** - Match UI to data needed
10. **Keep messages concise** - Users don't read long text

## Complete Example

See `examples/example_install.sh` for a complete working example with:
- All page types demonstrated
- Progress tracking
- Error handling
- Input validation
- Clean jq-based JSON parsing
