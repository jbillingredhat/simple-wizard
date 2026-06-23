# Simple Wizard - Scriptable Linux Installation Wizard
![Simple Wizard icon](./simple_wizard_icon.svg)


A GTK4-based installation wizard for Linux that can be controlled via scripts.
## Features

- Multi-pane layout with information sidebar, interaction area, and progress indicator
- Support for various prompt types: welcome, file/directory selection, password entry, questions, text input, warnings, errors, and completion
- Client-server architecture for scriptable control
- Progress tracking with customizable steps

## Requirements

- Python 3.8+
- GTK4
- PyGObject
- jq (for parsing JSON in bash scripts)

## Installation

```bash
# Install dependencies on Fedora
sudo dnf install python3-gobject gtk4 jq

# Install the package
pip install -e .
```

## Usage

See `examples/` directory for sample installation scripts.

## Documentation

- [QUICKSTART.md](docs/QUICKSTART.md) - Quick start guide
- [USAGE.md](docs/USAGE.md) - Detailed usage documentation
- [FEATURES.md](docs/FEATURES.md) - Feature reference
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Technical details
- [CHANGELOG.md](docs/CHANGELOG.md) - Version history

## License

Apache 2 License - see [LICENSE](LICENSE) file for details.
