"""Entry point to launch the autonomous sandbox."""
from __future__ import annotations

import argparse
from threading import Thread

from sandbox.config import load_config
from sandbox.services.daemon import Daemon
from sandbox.ui.app import create_app


def main() -> None:
    parser = argparse.ArgumentParser(description="Autonomous Sandbox")
    parser.add_argument("--preset", default="MAX", help="Configuration preset")
    parser.add_argument("--no-ui", action="store_true", help="Disable Flask UI")
    args = parser.parse_args()

    config = load_config(args.preset)
    if args.no_ui:
        config.enable_ui = False

    daemon = Daemon(config)
    daemon.start()

    if config.enable_ui:
        app = create_app()
        thread = Thread(target=lambda: app.run(host="0.0.0.0", port=5000), daemon=True)
        thread.start()
        thread.join()


def launchd_plist_example() -> str:
    return f"""
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>local.autonomous-sandbox</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>{__file__}</string>
    </array>
    <key>RunAtLoad</key><true/>
    <key>KeepAlive</key><true/>
    <key>StandardOutPath</key><string>logs/daemon.out.log</string>
    <key>StandardErrorPath</key><string>logs/daemon.err.log</string>
    <key>WorkingDirectory</key><string>{config.data_dir.parent}</string>
</dict>
</plist>
"""


if __name__ == "__main__":
    main()
