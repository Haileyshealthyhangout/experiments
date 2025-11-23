"""Routes for dashboard."""
from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify, render_template, request

from ..services.daemon import Daemon
from ..config import load_config


def register_routes(app: Flask) -> None:
    config = load_config("MAX")
    daemon = Daemon(config)
    daemon.start()

    @app.route("/")
    def index():
        memory = daemon.memory.load_all()
        return render_template(
            "index.html",
            identity=daemon.identity,
            memory=memory[-5:],
            last_snapshot=memory[-1] if memory else None,
            agents=[a.__dict__ for a in daemon.agents.agents],
            config=config,
        )

    @app.route("/sync/export")
    def export_state():
        path = daemon.sync.export_state()
        return jsonify({"export_path": str(path)})

    @app.route("/sync/import", methods=["POST"])
    def import_state():
        payload = request.json or {}
        daemon.sync.import_path.write_text(request.data.decode("utf-8"), encoding="utf-8")
        return jsonify({"status": "stored", "bytes": len(request.data)})

    @app.route("/controls/stop", methods=["POST"])
    def stop():
        daemon.stop()
        return jsonify({"status": "stopped"})

    @app.route("/controls/start", methods=["POST"])
    def start():
        daemon.start()
        return jsonify({"status": "started"})
