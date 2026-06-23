#!/usr/bin/env python3
"""
Example installation script using Simple Wizard Python API.

This demonstrates how to use the wizard from a Python script.
"""

import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent))

from simple_wizard.client import WizardClient


def main():
    """Run example installation."""
    client = WizardClient()

    # Set up the wizard information
    client.set_info(
        title="Python App Installer",
        description="This wizard will guide you through installing Python App.",
        help_text="Follow the prompts to complete the installation."
    )

    # Set total number of steps
    client.set_progress(total=7, current=0, status="Starting installation")

    # Step 1: Welcome
    client.set_progress(current=1, status="Welcome")
    response = client.show_welcome(
        title="Welcome to Python App Installer",
        message="This wizard will help you install Python App on your system.\n\n"
                "Click Next to begin the installation process."
    )
    print(f"Welcome response: {response}")

    # Step 2: Select installation directory
    client.set_progress(current=2, status="Selecting installation directory")
    response = client.show_directory(
        title="Installation Directory",
        message="Select where you want to install Python App.",
        default_path=str(Path.home() / "python-app")
    )

    if response.get('response', {}).get('action') == 'cancel':
        client.show_error(title="Installation Cancelled", message="Installation was cancelled by user.")
        client.quit()
        return 1

    install_dir = response.get('response', {}).get('path', '')
    print(f"Installation directory: {install_dir}")

    # Step 3: Select configuration file (optional)
    client.set_progress(current=3, status="Configuration file")
    response = client.show_file(
        title="Configuration File",
        message="Select a configuration file (optional).",
        default_path=""
    )
    config_file = response.get('response', {}).get('path', '')
    print(f"Configuration file: {config_file}")

    # Step 4: Password setup
    client.set_progress(current=4, status="Setting up password")
    response = client.show_password(
        title="Set Admin Password",
        message="Create a password for the admin account.",
        confirm=True
    )

    if response.get('response', {}).get('action') == 'cancel':
        client.show_error(title="Installation Cancelled", message="Installation was cancelled by user.")
        client.quit()
        return 1

    print("Password set successfully")

    # Step 5: User information (with email validation)
    client.set_progress(current=5, status="User information")
    response = client.show_text(
        title="User Information",
        message="Please enter your email address.",
        placeholder="user@example.com",
        validate="email"
    )
    email = response.get('response', {}).get('text', '')
    print(f"Email: {email}")

    # Step 6: Installation options
    client.set_progress(current=6, status="Installation options")
    response = client.show_question(
        title="Installation Type",
        message="What type of installation would you like?",
        buttons=["Full", "Minimal", "Custom"]
    )
    install_type = response.get('response', {}).get('button', '')
    print(f"Installation type: {install_type}")

    # Show warning before proceeding
    client.show_warning(
        title="Ready to Install",
        message=f"The installer is ready to install Python App.\n\n"
                f"Installation directory: {install_dir}\n"
                f"Installation type: {install_type}\n\n"
                f"Click OK to continue."
    )

    # Simulate installation with logging
    import time
    client.append_log(f"Starting installation to {install_dir}")
    client.append_log("Creating directory structure...")
    time.sleep(1)
    client.append_log("Installing Python packages...")
    time.sleep(1)
    client.append_log(f"Configuring for {install_type} installation...")
    client.append_log(f"Setting user email to {email}")
    time.sleep(1)
    client.append_log("Installation process complete!")

    # Step 7: Complete
    client.set_progress(current=7, status="Installation complete")
    client.show_complete(
        title="Installation Complete!",
        message=f"Python App has been successfully installed.\n\n"
                f"Installation directory: {install_dir}\n"
                f"Email: {email}\n"
                f"Installation type: {install_type}\n\n"
                f"Thank you for installing Python App!"
    )

    # Quit the wizard
    client.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
