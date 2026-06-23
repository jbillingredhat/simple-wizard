# Simple Wizard Architecture

## Overview

Simple Wizard uses a client-server architecture with Unix domain sockets for inter-process communication.

```
┌─────────────────────────────────────────────────────────────┐
│                      Installation Script                    │
│                    (Bash, Python, etc.)                     │
└────────────────────────────┬────────────────────────────────┘
                             │
                             │ Commands via
                             │ simple-wizard-client
                             │
                             ▼
                  ┌──────────────────────┐
                  │  Unix Domain Socket  │
                  │ /tmp/simple-wizard.sock │
                  └──────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────┐
│                      simple-wizard (GTK4)                     │
├────────────────────────────────────────────────────────────┤
│  ┌───────────────────────┬─────────────────────────────┐   │
│  │   Info Panel          │   Content Area              │   │
│  │   (Left Sidebar)      │   (Page Display)            │   │
│  │                       │                             │   │
│  │  • Icon               │  • Welcome Page             │   │
│  │  • Title              │  • File/Dir Selection       │   │
│  │  • Description        │  • Password Entry           │   │
│  │  • Help Text          │  • Question Dialog          │   │
│  │                       │  • Text Input               │   │
│  │                       │  • Warning/Error/Complete   │   │
│  └───────────────────────┴─────────────────────────────┘   │
│  ┌───────────────────────────────────────────────────────┐ │
│  │   Progress Panel (Bottom)                             │ │
│  │   • Progress Bar                                      │ │
│  │   • Status Text                                       │ │
│  └───────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘
```

## Component Structure

### 1. Wizard Server (`simple_wizard/wizard.py`)

**WizardWindow**
- Main GTK4 window with three-pane layout
- Top-left: Information panel (icon, title, description, help)
- Top-right: Content area (interactive pages)
- Bottom: Progress bar and status text

**WizardApplication**
- GTK Application managing the window lifecycle
- Runs Unix socket server in background thread
- Processes commands from client
- Marshals responses between GTK main thread and socket thread

**Threading Model**
- Main thread: GTK event loop
- Background thread: Socket server
- `GLib.idle_add()`: Bridge commands to GTK main thread
- `threading.Event`: Wait for user responses

### 2. Client Library (`simple_wizard/client.py`)

**WizardClient**
- Python API for controlling the wizard
- Methods for each page type
- JSON-based protocol over Unix socket

**Command-line Interface**
- Subcommand-based CLI (`argparse`)
- Maps CLI args to WizardClient methods
- Outputs JSON responses

### 3. Page System (`simple_wizard/pages.py`)

**BasePage**
- Abstract base class for all pages
- Manages widget container and callbacks

**Page Types**
- `WelcomePage`: Informational page with Next button
- `FilePage`: File chooser with text entry and browse button
- `DirectoryPage`: Directory chooser with text entry
- `PasswordPage`: Password entry with optional confirmation
- `QuestionPage`: Multiple choice buttons
- `TextEntryPage`: Single-line text input
- `WarningPage`: Warning icon and message
- `ErrorPage`: Error icon and message
- `CompletePage`: Success icon and message

Each page:
- Builds its UI in `__init__`
- Calls callback with response dictionary when user interacts
- Returns control to wizard for next command

## Communication Protocol

### Command Format (Client → Server)

```json
{
  "command": "show_page",
  "page_type": "directory",
  "params": {
    "title": "Select Directory",
    "message": "Choose install location",
    "default_path": "/home/user/app"
  }
}
```

### Response Format (Server → Client)

```json
{
  "status": "ok",
  "response": {
    "action": "next",
    "path": "/home/user/selected/path"
  }
}
```

### Command Types

- `set_info`: Update information panel
- `set_progress`: Update progress bar/status
- `show_page`: Display a page and wait for user input
- `quit`: Close the wizard

## Execution Flow

1. **Wizard starts**: Opens GTK window, starts socket server
2. **Script sends command**: Client connects to socket, sends JSON command
3. **Server receives**: Background thread receives command
4. **Marshal to GTK**: Command posted to main thread via `GLib.idle_add()`
5. **Display page**: Page widgets created and displayed
6. **User interacts**: Clicks button, enters text, etc.
7. **Callback fires**: Page calls `response_callback` with result
8. **Response sent**: Result marshaled back to socket thread
9. **Client receives**: JSON response returned to script
10. **Script continues**: Processes response, sends next command

## Synchronization

The wizard uses synchronous request-response:

1. Client sends command and **blocks** waiting for response
2. Server processes command and **blocks** waiting for user
3. User completes interaction
4. Response returned to client
5. Client unblocks and returns response to script

This ensures:
- Script execution matches user pace
- No command queueing complexity
- Simple linear script flow

## File Organization

```
simple_wizard/
├── __init__.py          # Package initialization
├── wizard.py            # GTK application, window, socket server
├── pages.py             # Page implementations
└── client.py            # Client library and CLI

examples/
├── example_install.sh   # Bash example
└── example_install.py   # Python example
```

## Extension Points

### Adding New Page Types

1. Create new class in `pages.py` inheriting from `BasePage`
2. Implement `__init__` to build UI
3. Call `self.callback(response_dict)` when complete
4. Add to `page_classes` dict in `WizardWindow.show_page()`
5. Add method to `WizardClient` class
6. Add CLI subcommand in `client.py`

### Custom Styling

GTK4 CSS can be applied to widgets using CSS classes:
- `info-panel`: Left sidebar
- `suggested-action`: Primary buttons (blue)
- `destructive-action`: Danger buttons (red)
- `error`: Error labels

### Socket Security

Current implementation uses:
- Unix domain sockets (local only)
- File system permissions control access
- Single client at a time

For production:
- Consider authentication tokens
- Validate command parameters
- Rate limiting
- Audit logging

## Dependencies

- **GTK4**: UI toolkit (libgtk-4)
- **PyGObject**: Python bindings for GTK
- **Python 3.8+**: Standard library only (socket, json, threading)

No external Python packages required beyond PyGObject.

## Platform Notes

**Fedora Linux**
- Native GTK4 support
- Install via: `dnf install gtk4 python3-gobject`

**Other Distributions**
- GTK4 must be available (version 4.0+)
- PyGObject 3.42+ recommended
- May need `python3-gi` or similar package

**File Dialogs**
- Uses `Gtk.FileDialog` (GTK 4.10+)
- Falls back gracefully on older GTK4 versions
- Native file choosers on most desktops
