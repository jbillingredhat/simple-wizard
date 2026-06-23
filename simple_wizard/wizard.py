#!/usr/bin/env python3
"""
Main wizard window implementation with GTK4.
"""

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib, Gio
import sys
import socket
import threading
import json
from pathlib import Path

from .pages import (
    WelcomePage, FilePage, DirectoryPage, PasswordPage,
    QuestionPage, TextEntryPage, WarningPage, ErrorPage, CompletePage
)


class WizardWindow(Gtk.ApplicationWindow):
    """Main wizard window with three-pane layout."""

    def __init__(self, application, title="Installation Wizard", icon_name=None):
        super().__init__(application=application)

        self.set_title(title)
        self.set_default_size(800, 600)

        self.total_steps = 0
        self.current_step = 0
        self.current_page = None
        self.response_callback = None

        # Main vertical box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_child(main_box)

        # Top paned widget (two columns)
        top_paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        top_paned.set_vexpand(True)
        main_box.append(top_paned)

        # Left sidebar (info panel)
        self.info_panel = self._create_info_panel(icon_name)
        top_paned.set_start_child(self.info_panel)
        top_paned.set_resize_start_child(False)
        top_paned.set_shrink_start_child(False)

        # Right content area (interaction panel)
        self.content_frame = Gtk.Frame()
        self.content_frame.set_margin_top(12)
        self.content_frame.set_margin_end(12)
        self.content_frame.set_margin_bottom(12)

        self.content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.content_box.set_margin_start(24)
        self.content_box.set_margin_end(24)
        self.content_box.set_margin_top(24)
        self.content_box.set_margin_bottom(24)
        self.content_frame.set_child(self.content_box)

        top_paned.set_end_child(self.content_frame)
        top_paned.set_resize_end_child(True)
        top_paned.set_shrink_end_child(False)

        # Set position of the divider (left panel width)
        top_paned.set_position(250)

        # Bottom progress panel
        self.progress_panel = self._create_progress_panel()
        main_box.append(self.progress_panel)

        # Expandable log panel
        self.log_expander = self._create_log_panel()
        main_box.append(self.log_expander)

    def _create_info_panel(self, icon_name):
        """Create the left information panel."""
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.add_css_class("info-panel")
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_margin_top(12)
        box.set_margin_bottom(12)

        # Icon
        if icon_name:
            self.info_icon = Gtk.Image.new_from_icon_name(icon_name)
            self.info_icon.set_pixel_size(64)
        else:
            self.info_icon = Gtk.Image.new_from_icon_name("application-x-executable")
            self.info_icon.set_pixel_size(64)
        self.info_icon.set_margin_top(12)
        box.append(self.info_icon)

        # Title
        self.info_title = Gtk.Label()
        self.info_title.set_markup("<b>Installation Wizard</b>")
        self.info_title.set_wrap(True)
        self.info_title.set_margin_top(12)
        box.append(self.info_title)

        # Description
        self.info_description = Gtk.Label()
        self.info_description.set_text("Follow the steps to complete the installation.")
        self.info_description.set_wrap(True)
        self.info_description.set_margin_top(6)
        box.append(self.info_description)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(12)
        box.append(separator)

        # Help text
        self.info_help = Gtk.Label()
        self.info_help.set_text("")
        self.info_help.set_wrap(True)
        self.info_help.set_justify(Gtk.Justification.LEFT)
        self.info_help.set_xalign(0)
        self.info_help.set_vexpand(True)
        self.info_help.set_valign(Gtk.Align.START)
        box.append(self.info_help)

        return box

    def _create_progress_panel(self):
        """Create the bottom progress panel."""
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_margin_top(6)
        box.set_margin_bottom(12)

        # Progress bar
        self.progress_bar = Gtk.ProgressBar()
        self.progress_bar.set_show_text(False)
        box.append(self.progress_bar)

        # Status label
        self.status_label = Gtk.Label()
        self.status_label.set_xalign(0)
        self.status_label.set_text("Ready")
        box.append(self.status_label)

        return box

    def _create_log_panel(self):
        """Create the expandable log panel."""
        expander = Gtk.Expander()
        expander.set_label("Installation Log")
        expander.set_expanded(False)
        expander.set_margin_start(12)
        expander.set_margin_end(12)
        expander.set_margin_bottom(12)

        # Scrolled window for log
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_min_content_height(150)
        scrolled.set_max_content_height(300)
        scrolled.set_vexpand(False)

        # Text view for log messages
        self.log_buffer = Gtk.TextBuffer()
        self.log_view = Gtk.TextView(buffer=self.log_buffer)
        self.log_view.set_editable(False)
        self.log_view.set_cursor_visible(False)
        self.log_view.set_monospace(True)
        self.log_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.log_view.set_margin_start(6)
        self.log_view.set_margin_end(6)
        self.log_view.set_margin_top(6)
        self.log_view.set_margin_bottom(6)

        scrolled.set_child(self.log_view)
        expander.set_child(scrolled)

        return expander

    def append_log(self, message):
        """Append a message to the log."""
        end_iter = self.log_buffer.get_end_iter()
        self.log_buffer.insert(end_iter, message + "\n")

        # Auto-scroll to bottom
        end_mark = self.log_buffer.create_mark(None, self.log_buffer.get_end_iter(), False)
        self.log_view.scroll_to_mark(end_mark, 0.0, True, 0.0, 1.0)
        self.log_buffer.delete_mark(end_mark)

    def clear_log(self):
        """Clear the log."""
        self.log_buffer.set_text("")

    def set_info(self, title=None, description=None, help_text=None):
        """Update the information panel."""
        if title:
            self.info_title.set_markup(f"<b>{title}</b>")
        if description:
            self.info_description.set_text(description)
        if help_text:
            self.info_help.set_text(help_text)

    def set_progress(self, current=None, total=None, status=None):
        """Update progress bar and status."""
        if total is not None:
            self.total_steps = total
        if current is not None:
            self.current_step = current
        if status:
            self.status_label.set_text(status)

        if self.total_steps > 0:
            fraction = self.current_step / self.total_steps
            self.progress_bar.set_fraction(fraction)
            self.progress_bar.set_visible(True)
        else:
            self.progress_bar.set_visible(False)

    def show_page(self, page_type, **kwargs):
        """Display a page and wait for user response."""
        # Clear current content
        while child := self.content_box.get_first_child():
            self.content_box.remove(child)

        # Create the appropriate page
        page_classes = {
            'welcome': WelcomePage,
            'file': FilePage,
            'directory': DirectoryPage,
            'password': PasswordPage,
            'question': QuestionPage,
            'text': TextEntryPage,
            'warning': WarningPage,
            'error': ErrorPage,
            'complete': CompletePage,
        }

        page_class = page_classes.get(page_type)
        if not page_class:
            raise ValueError(f"Unknown page type: {page_type}")

        self.current_page = page_class(self.content_box, self._on_page_response, **kwargs)

        # Update status if provided
        if 'status' in kwargs:
            self.status_label.set_text(kwargs['status'])

    def _on_page_response(self, response):
        """Handle page response."""
        if self.response_callback:
            self.response_callback(response)


class WizardApplication(Gtk.Application):
    """GTK Application for the wizard."""

    def __init__(self, socket_path="/tmp/simple-wizard.sock"):
        super().__init__(application_id="com.redhat.jbilling.simplewizard",
                        flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.window = None
        self.socket_path = socket_path
        self.server_thread = None
        self.running = True

    def do_activate(self):
        """Activate the application."""
        if not self.window:
            self.window = WizardWindow(self, title="Installation Wizard")
        self.window.present()

        # Start socket server in a background thread
        if not self.server_thread:
            self.server_thread = threading.Thread(target=self._run_server, daemon=True)
            self.server_thread.start()

    def _run_server(self):
        """Run the Unix socket server."""
        # Remove existing socket file
        try:
            Path(self.socket_path).unlink()
        except FileNotFoundError:
            pass

        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(self.socket_path)
        server.listen(1)
        server.settimeout(1.0)  # Timeout to check running flag

        while self.running:
            try:
                conn, _ = server.accept()
                threading.Thread(target=self._handle_client, args=(conn,), daemon=True).start()
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Server error: {e}")
                break

        server.close()
        try:
            Path(self.socket_path).unlink()
        except:
            pass

    def _handle_client(self, conn):
        """Handle a client connection."""
        try:
            data = b""
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                data += chunk
                if b"\n" in data:
                    break

            if data:
                message = json.loads(data.decode('utf-8'))
                response = self._process_command(message)
                conn.sendall(json.dumps(response).encode('utf-8') + b"\n")
        except Exception as e:
            error_response = {"status": "error", "message": str(e)}
            conn.sendall(json.dumps(error_response).encode('utf-8') + b"\n")
        finally:
            conn.close()

    def _process_command(self, message):
        """Process a command from the client."""
        cmd = message.get('command')

        if cmd == 'set_info':
            GLib.idle_add(self.window.set_info,
                         message.get('title'),
                         message.get('description'),
                         message.get('help_text'))
            return {"status": "ok"}

        elif cmd == 'set_progress':
            GLib.idle_add(self.window.set_progress,
                         message.get('current'),
                         message.get('total'),
                         message.get('status'))
            return {"status": "ok"}

        elif cmd == 'show_page':
            # This needs to wait for user response
            response_data = {}
            response_event = threading.Event()

            def callback(resp):
                response_data['response'] = resp
                response_event.set()

            def show_page_wrapper():
                self.window.show_page(message['page_type'], **message.get('params', {}))
                return False  # Don't repeat

            self.window.response_callback = callback
            GLib.idle_add(show_page_wrapper)

            # Wait for response (with timeout)
            response_event.wait(timeout=300)  # 5 minute timeout
            self.window.response_callback = None

            return {"status": "ok", "response": response_data.get('response')}

        elif cmd == 'append_log':
            GLib.idle_add(self.window.append_log, message.get('message', ''))
            return {"status": "ok"}

        elif cmd == 'clear_log':
            GLib.idle_add(self.window.clear_log)
            return {"status": "ok"}

        elif cmd == 'quit':
            GLib.idle_add(self.quit)
            return {"status": "ok"}

        else:
            return {"status": "error", "message": f"Unknown command: {cmd}"}


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="SImple Installation Wizard")
    parser.add_argument("--socket", default="/tmp/simple-wizard.sock",
                       help="Unix socket path for IPC")
    args = parser.parse_args()

    app = WizardApplication(socket_path=args.socket)
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
