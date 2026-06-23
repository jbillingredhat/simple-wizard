#!/usr/bin/env python3
"""
Page implementations for different interaction types.
"""

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
import re


# Validation regex presets
VALIDATION_PRESETS = {
    'email': (
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        'Please enter a valid email address (e.g., user@example.com)'
    ),
    'url': (
        r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$',
        'Please enter a valid URL (e.g., https://example.com)'
    ),
    'ipv4': (
        r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$',
        'Please enter a valid IPv4 address (e.g., 192.168.1.1)'
    ),
    'port': (
        r'^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$',
        'Please enter a valid port number (1-65535)'
    ),
    'hostname': (
        r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$',
        'Please enter a valid hostname (e.g., example.com)'
    ),
    'username': (
        r'^[a-zA-Z0-9_-]{3,32}$',
        'Please enter a valid username (3-32 alphanumeric characters, dashes, or underscores)'
    ),
    'number': (
        r'^-?\d+$',
        'Please enter a valid number'
    ),
    'positive_number': (
        r'^\d+$',
        'Please enter a positive number'
    ),
    'alphanumeric': (
        r'^[a-zA-Z0-9]+$',
        'Please enter only letters and numbers'
    ),
}


class BasePage:
    """Base class for all pages."""

    def __init__(self, container, callback):
        self.container = container
        self.callback = callback

    def _add_widget(self, widget):
        """Helper to add widget to container."""
        self.container.append(widget)


class WelcomePage(BasePage):
    """Welcome page with text and Next button."""

    def __init__(self, container, callback, title="Welcome", message="", **kwargs):
        super().__init__(container, callback)

        # Title
        title_label = Gtk.Label()
        title_label.set_markup(f"<span size='x-large' weight='bold'>{title}</span>")
        title_label.set_xalign(0)
        title_label.set_margin_bottom(12)
        self._add_widget(title_label)

        # Message
        message_label = Gtk.Label(label=message)
        message_label.set_wrap(True)
        message_label.set_xalign(0)
        message_label.set_vexpand(True)
        message_label.set_valign(Gtk.Align.START)
        self._add_widget(message_label)

        # Button box
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        button_box.set_halign(Gtk.Align.END)
        self._add_widget(button_box)

        # Next button
        next_button = Gtk.Button(label="Next")
        next_button.add_css_class("suggested-action")
        next_button.connect("clicked", lambda _: self.callback({"action": "next"}))
        button_box.append(next_button)


class FilePage(BasePage):
    """File selection page."""

    def __init__(self, container, callback, title="Select File", message="", default_path="", **kwargs):
        super().__init__(container, callback)

        # Title
        title_label = Gtk.Label()
        title_label.set_markup(f"<span size='large' weight='bold'>{title}</span>")
        title_label.set_xalign(0)
        title_label.set_margin_bottom(12)
        self._add_widget(title_label)

        # Message
        if message:
            message_label = Gtk.Label(label=message)
            message_label.set_wrap(True)
            message_label.set_xalign(0)
            message_label.set_margin_bottom(12)
            self._add_widget(message_label)

        # File chooser row
        file_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        file_box.set_margin_bottom(12)
        self._add_widget(file_box)

        self.entry = Gtk.Entry()
        self.entry.set_text(default_path)
        self.entry.set_hexpand(True)
        file_box.append(self.entry)

        browse_button = Gtk.Button(label="Browse...")
        browse_button.connect("clicked", self._on_browse)
        file_box.append(browse_button)

        # Spacer
        spacer = Gtk.Box()
        spacer.set_vexpand(True)
        self._add_widget(spacer)

        # Button box
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        button_box.set_halign(Gtk.Align.END)
        self._add_widget(button_box)

        cancel_button = Gtk.Button(label="Cancel")
        cancel_button.connect("clicked", lambda _: self.callback({"action": "cancel"}))
        button_box.append(cancel_button)

        next_button = Gtk.Button(label="Next")
        next_button.add_css_class("suggested-action")
        next_button.connect("clicked", self._on_next)
        button_box.append(next_button)

        # Store window reference for file dialog
        self.window = None
        widget = container
        while widget:
            if isinstance(widget, Gtk.Window):
                self.window = widget
                break
            widget = widget.get_parent()

    def _on_browse(self, button):
        """Open file chooser dialog."""
        dialog = Gtk.FileDialog()
        dialog.open(self.window, None, self._on_file_selected)

    def _on_file_selected(self, dialog, result):
        """Handle file selection."""
        try:
            file = dialog.open_finish(result)
            if file:
                self.entry.set_text(file.get_path())
        except:
            pass

    def _on_next(self, button):
        """Handle next button click."""
        path = self.entry.get_text()
        self.callback({"action": "next", "path": path})


class DirectoryPage(BasePage):
    """Directory selection page."""

    def __init__(self, container, callback, title="Select Directory", message="", default_path="", **kwargs):
        super().__init__(container, callback)

        # Title
        title_label = Gtk.Label()
        title_label.set_markup(f"<span size='large' weight='bold'>{title}</span>")
        title_label.set_xalign(0)
        title_label.set_margin_bottom(12)
        self._add_widget(title_label)

        # Message
        if message:
            message_label = Gtk.Label(label=message)
            message_label.set_wrap(True)
            message_label.set_xalign(0)
            message_label.set_margin_bottom(12)
            self._add_widget(message_label)

        # Directory chooser row
        dir_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        dir_box.set_margin_bottom(12)
        self._add_widget(dir_box)

        self.entry = Gtk.Entry()
        self.entry.set_text(default_path)
        self.entry.set_hexpand(True)
        dir_box.append(self.entry)

        browse_button = Gtk.Button(label="Browse...")
        browse_button.connect("clicked", self._on_browse)
        dir_box.append(browse_button)

        # Spacer
        spacer = Gtk.Box()
        spacer.set_vexpand(True)
        self._add_widget(spacer)

        # Button box
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        button_box.set_halign(Gtk.Align.END)
        self._add_widget(button_box)

        cancel_button = Gtk.Button(label="Cancel")
        cancel_button.connect("clicked", lambda _: self.callback({"action": "cancel"}))
        button_box.append(cancel_button)

        next_button = Gtk.Button(label="Next")
        next_button.add_css_class("suggested-action")
        next_button.connect("clicked", self._on_next)
        button_box.append(next_button)

        # Store window reference for dialog
        self.window = None
        widget = container
        while widget:
            if isinstance(widget, Gtk.Window):
                self.window = widget
                break
            widget = widget.get_parent()

    def _on_browse(self, button):
        """Open directory chooser dialog."""
        dialog = Gtk.FileDialog()
        dialog.select_folder(self.window, None, self._on_folder_selected)

    def _on_folder_selected(self, dialog, result):
        """Handle folder selection."""
        try:
            file = dialog.select_folder_finish(result)
            if file:
                self.entry.set_text(file.get_path())
        except:
            pass

    def _on_next(self, button):
        """Handle next button click."""
        path = self.entry.get_text()
        self.callback({"action": "next", "path": path})


class PasswordPage(BasePage):
    """Password entry page with optional confirmation."""

    def __init__(self, container, callback, title="Enter Password", message="",
                 confirm=True, **kwargs):
        super().__init__(container, callback)

        # Title
        title_label = Gtk.Label()
        title_label.set_markup(f"<span size='large' weight='bold'>{title}</span>")
        title_label.set_xalign(0)
        title_label.set_margin_bottom(12)
        self._add_widget(title_label)

        # Message
        if message:
            message_label = Gtk.Label(label=message)
            message_label.set_wrap(True)
            message_label.set_xalign(0)
            message_label.set_margin_bottom(12)
            self._add_widget(message_label)

        # Password entry
        password_label = Gtk.Label(label="Password:")
        password_label.set_xalign(0)
        self._add_widget(password_label)

        self.password_entry = Gtk.PasswordEntry()
        self.password_entry.set_show_peek_icon(True)
        self.password_entry.set_margin_bottom(12)
        self._add_widget(self.password_entry)

        # Confirmation entry
        self.confirm_entry = None
        if confirm:
            confirm_label = Gtk.Label(label="Confirm Password:")
            confirm_label.set_xalign(0)
            self._add_widget(confirm_label)

            self.confirm_entry = Gtk.PasswordEntry()
            self.confirm_entry.set_show_peek_icon(True)
            self.confirm_entry.set_margin_bottom(12)
            self._add_widget(self.confirm_entry)

        # Error label (hidden by default)
        self.error_label = Gtk.Label()
        self.error_label.add_css_class("error")
        self.error_label.set_xalign(0)
        self.error_label.set_visible(False)
        self._add_widget(self.error_label)

        # Spacer
        spacer = Gtk.Box()
        spacer.set_vexpand(True)
        self._add_widget(spacer)

        # Button box
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        button_box.set_halign(Gtk.Align.END)
        self._add_widget(button_box)

        cancel_button = Gtk.Button(label="Cancel")
        cancel_button.connect("clicked", lambda _: self.callback({"action": "cancel"}))
        button_box.append(cancel_button)

        next_button = Gtk.Button(label="Next")
        next_button.add_css_class("suggested-action")
        next_button.connect("clicked", self._on_next)
        button_box.append(next_button)

    def _on_next(self, button):
        """Handle next button click."""
        password = self.password_entry.get_text()

        if self.confirm_entry:
            confirm = self.confirm_entry.get_text()
            if password != confirm:
                self.error_label.set_text("Passwords do not match!")
                self.error_label.set_visible(True)
                return

        self.callback({"action": "next", "password": password})


class QuestionPage(BasePage):
    """Question page with multiple button options."""

    def __init__(self, container, callback, title="Question", message="",
                 buttons=None, **kwargs):
        super().__init__(container, callback)

        if buttons is None:
            buttons = ["Yes", "No"]

        # Title
        title_label = Gtk.Label()
        title_label.set_markup(f"<span size='large' weight='bold'>{title}</span>")
        title_label.set_xalign(0)
        title_label.set_margin_bottom(12)
        self._add_widget(title_label)

        # Message
        message_label = Gtk.Label(label=message)
        message_label.set_wrap(True)
        message_label.set_xalign(0)
        message_label.set_vexpand(True)
        message_label.set_valign(Gtk.Align.START)
        self._add_widget(message_label)

        # Button box
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        button_box.set_halign(Gtk.Align.END)
        self._add_widget(button_box)

        # Create buttons
        for i, button_text in enumerate(buttons):
            btn = Gtk.Button(label=button_text)
            if i == 0:
                btn.add_css_class("suggested-action")
            btn.connect("clicked", lambda b, text=button_text:
                       self.callback({"action": "button", "button": text}))
            button_box.append(btn)


class TextEntryPage(BasePage):
    """Simple text entry page with optional validation."""

    def __init__(self, container, callback, title="Enter Text", message="",
                 default_text="", placeholder="", validate=None,
                 validation_message=None, **kwargs):
        super().__init__(container, callback)

        # Set up validation
        self.validation_regex = None
        self.validation_message = validation_message

        if validate:
            # Check if it's a preset
            if validate in VALIDATION_PRESETS:
                self.validation_regex = VALIDATION_PRESETS[validate][0]
                if not validation_message:
                    self.validation_message = VALIDATION_PRESETS[validate][1]
            else:
                # Custom regex
                self.validation_regex = validate
                if not validation_message:
                    self.validation_message = "Please enter a valid value"

        # Title
        title_label = Gtk.Label()
        title_label.set_markup(f"<span size='large' weight='bold'>{title}</span>")
        title_label.set_xalign(0)
        title_label.set_margin_bottom(12)
        self._add_widget(title_label)

        # Message
        if message:
            message_label = Gtk.Label(label=message)
            message_label.set_wrap(True)
            message_label.set_xalign(0)
            message_label.set_margin_bottom(12)
            self._add_widget(message_label)

        # Text entry
        self.entry = Gtk.Entry()
        self.entry.set_text(default_text)
        if placeholder:
            self.entry.set_placeholder_text(placeholder)
        self.entry.set_margin_bottom(6)
        self._add_widget(self.entry)

        # Error label (hidden by default)
        self.error_label = Gtk.Label()
        self.error_label.add_css_class("error")
        self.error_label.set_xalign(0)
        self.error_label.set_visible(False)
        self.error_label.set_margin_bottom(12)
        self._add_widget(self.error_label)

        # Spacer
        spacer = Gtk.Box()
        spacer.set_vexpand(True)
        self._add_widget(spacer)

        # Button box
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        button_box.set_halign(Gtk.Align.END)
        self._add_widget(button_box)

        cancel_button = Gtk.Button(label="Cancel")
        cancel_button.connect("clicked", lambda _: self.callback({"action": "cancel"}))
        button_box.append(cancel_button)

        next_button = Gtk.Button(label="Next")
        next_button.add_css_class("suggested-action")
        next_button.connect("clicked", self._on_next)
        button_box.append(next_button)

    def _on_next(self, button):
        """Handle next button click."""
        text = self.entry.get_text()

        # Validate if regex is set
        if self.validation_regex:
            if not re.match(self.validation_regex, text):
                self.error_label.set_text(self.validation_message)
                self.error_label.set_visible(True)
                return

        # Validation passed or no validation
        self.callback({"action": "next", "text": text})


class WarningPage(BasePage):
    """Warning page with OK button."""

    def __init__(self, container, callback, title="Warning", message="", **kwargs):
        super().__init__(container, callback)

        # Icon
        icon = Gtk.Image.new_from_icon_name("dialog-warning")
        icon.set_pixel_size(48)
        icon.set_margin_bottom(12)
        self._add_widget(icon)

        # Title
        title_label = Gtk.Label()
        title_label.set_markup(f"<span size='large' weight='bold'>{title}</span>")
        title_label.set_margin_bottom(12)
        self._add_widget(title_label)

        # Message
        message_label = Gtk.Label(label=message)
        message_label.set_wrap(True)
        message_label.set_justify(Gtk.Justification.CENTER)
        message_label.set_vexpand(True)
        message_label.set_valign(Gtk.Align.START)
        self._add_widget(message_label)

        # Button box
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        button_box.set_halign(Gtk.Align.CENTER)
        self._add_widget(button_box)

        ok_button = Gtk.Button(label="OK")
        ok_button.add_css_class("suggested-action")
        ok_button.connect("clicked", lambda _: self.callback({"action": "ok"}))
        button_box.append(ok_button)


class ErrorPage(BasePage):
    """Error page."""

    def __init__(self, container, callback, title="Error", message="", **kwargs):
        super().__init__(container, callback)

        # Icon
        icon = Gtk.Image.new_from_icon_name("dialog-error")
        icon.set_pixel_size(48)
        icon.set_margin_bottom(12)
        self._add_widget(icon)

        # Title
        title_label = Gtk.Label()
        title_label.set_markup(f"<span size='large' weight='bold'>{title}</span>")
        title_label.set_margin_bottom(12)
        self._add_widget(title_label)

        # Message
        message_label = Gtk.Label(label=message)
        message_label.set_wrap(True)
        message_label.set_justify(Gtk.Justification.CENTER)
        message_label.set_vexpand(True)
        message_label.set_valign(Gtk.Align.START)
        self._add_widget(message_label)

        # Button box
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        button_box.set_halign(Gtk.Align.CENTER)
        self._add_widget(button_box)

        ok_button = Gtk.Button(label="OK")
        ok_button.add_css_class("destructive-action")
        ok_button.connect("clicked", lambda _: self.callback({"action": "ok"}))
        button_box.append(ok_button)


class CompletePage(BasePage):
    """Completion page."""

    def __init__(self, container, callback, title="Complete", message="Installation completed successfully!", **kwargs):
        super().__init__(container, callback)

        # Icon
        icon = Gtk.Image.new_from_icon_name("emblem-ok-symbolic")
        icon.set_pixel_size(64)
        icon.set_margin_bottom(12)
        self._add_widget(icon)

        # Title
        title_label = Gtk.Label()
        title_label.set_markup(f"<span size='x-large' weight='bold'>{title}</span>")
        title_label.set_margin_bottom(12)
        self._add_widget(title_label)

        # Message
        message_label = Gtk.Label(label=message)
        message_label.set_wrap(True)
        message_label.set_justify(Gtk.Justification.CENTER)
        message_label.set_vexpand(True)
        message_label.set_valign(Gtk.Align.START)
        self._add_widget(message_label)

        # Button box
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        button_box.set_halign(Gtk.Align.CENTER)
        self._add_widget(button_box)

        finish_button = Gtk.Button(label="Finish")
        finish_button.add_css_class("suggested-action")
        finish_button.connect("clicked", lambda _: self.callback({"action": "finish"}))
        button_box.append(finish_button)
