# Changelog

All notable changes to Simple Wizard will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-06-23

### Added

#### Core Features
- GTK4-based installation wizard with three-pane layout
  - Left sidebar: Application icon, title, description, and help text
  - Right content area: Interactive pages for user input
  - Bottom panel: Progress bar and status text
- Client-server architecture using Unix domain sockets for IPC
- JSON-based communication protocol
- Both command-line and Python API interfaces

#### Page Types
- **Welcome Page** - Informational page with Next button
- **File Selection** - File chooser with text entry and browse button
- **Directory Selection** - Directory chooser with text entry and browse button
- **Password Entry** - Password input with optional confirmation field
- **Question Page** - Multiple choice buttons (customizable)
- **Text Entry** - Single-line text input with optional validation
- **Warning Page** - Warning message with OK button
- **Error Page** - Error message with OK button
- **Complete Page** - Success/completion message with Finish button

#### Validation System
- Text entry validation with regex support
- 9 built-in validation presets:
  - `email` - Valid email address
  - `url` - Valid HTTP/HTTPS URL
  - `ipv4` - Valid IPv4 address
  - `port` - Valid port number (1-65535)
  - `hostname` - Valid hostname
  - `username` - Alphanumeric username (3-32 characters)
  - `number` - Any integer
  - `positive_number` - Positive integer only
  - `alphanumeric` - Letters and numbers only
- Custom regex validation support
- Custom error messages
- Visual error feedback in UI

#### Logging System
- Expandable log panel at bottom of window
- Collapsible with disclosure triangle
- Auto-scrolling to latest messages
- Monospace text display
- Commands: `log` (append message), `clear-log` (clear all messages)

#### Progress Tracking
- Configurable progress bar
- Current step / total steps display
- Status text updates
- Optional (hidden when total steps = 0)

#### Client Commands
- `set-info` - Update wizard information panel
- `set-progress` - Update progress bar and status
- `welcome` - Show welcome page
- `file` - Show file selection page
- `directory` - Show directory selection page
- `password` - Show password entry page
- `question` - Show question page with custom buttons
- `text` - Show text entry page (with optional validation)
- `warning` - Show warning page
- `error` - Show error page
- `complete` - Show completion page
- `log` - Append message to log panel
- `clear-log` - Clear log panel
- `quit` - Close the wizard

#### Python API
- `WizardClient` class for programmatic control
- Methods for all page types
- Clean, type-hinted interface
- Support for all features (validation, logging, etc.)

#### Examples and Documentation
- Bash installation script example (`examples/example_install.sh`)
- Python installation script example (`examples/example_install.py`)
- Basic functionality test script (`test_wizard.sh`)
- Log panel demonstration script (`test_log.sh`)
- Validation demonstration script (`test_validation.sh`)
- Comprehensive documentation:
  - `README.md` - Project overview
  - `QUICKSTART.md` - Quick reference guide
  - `USAGE.md` - Detailed usage documentation
  - `ARCHITECTURE.md` - Technical architecture details
  - `FEATURES.md` - Feature reference and patterns
  - `PROJECT_SUMMARY.md` - Complete project summary

#### Build and Installation
- `setup.py` for Python package installation
- `Makefile` with convenience targets:
  - `make deps` - Install system dependencies
  - `make dev` - Install in development mode
  - `make run` - Run wizard server
  - `make test` - Run basic tests
  - `make test-log` - Test log panel
  - `make test-validation` - Test validation
  - `make example-sh` - Run bash example
  - `make example-py` - Run Python example
  - `make clean` - Clean build artifacts
- Entry points: `simple-wizard` (server), `simple-wizard-client` (client)

#### Dependencies
- Python 3.8+
- GTK4 (4.0+)
- PyGObject (3.42+)
- jq (for JSON parsing in bash scripts)

### Fixed
- Fixed `GLib.idle_add()` keyword argument issue by using wrapper functions
- Fixed completion page "Finish" button in test scripts to properly wait for user action

### Technical Details
- Synchronous request-response model for simple script flow
- Background thread for socket server
- GTK main loop in main thread
- Thread-safe communication via `GLib.idle_add()`
- 5-minute timeout per page interaction
- Socket path: `/tmp/simple-wizard.sock` (configurable)

### License
- Apache 2.0 License

---

## Release Statistics

- **Total Lines of Code**: ~2,800+
- **Python Code**: ~1,200 lines
- **Documentation**: ~1,400+ lines
- **Examples and Tests**: ~400 lines
- **Files Created**: 20+

[0.1.0]: https://github.com/jbillingredhat/simple-wizard/releases/tag/v0.1.0
