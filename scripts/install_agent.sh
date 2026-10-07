#!/usr/bin/env bash
# Install the OpsWatch agent as a systemd service on a Linux host.
# Usage: sudo ./scripts/install_agent.sh
set -euo pipefail

INSTALL_DIR=/opt/opswatch-agent
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

mkdir -p "$INSTALL_DIR"
cp -r "$REPO_ROOT/agent/opswatch_agent" "$INSTALL_DIR/"
[ -f "$INSTALL_DIR/config.yaml" ] || cp "$REPO_ROOT/agent/config.example.yaml" "$INSTALL_DIR/config.yaml"

python3 -m venv "$INSTALL_DIR/.venv"
"$INSTALL_DIR/.venv/bin/pip" install -q -r "$REPO_ROOT/agent/requirements.txt"

cat > /etc/systemd/system/opswatch-agent.service <<UNIT
[Unit]
Description=OpsWatch monitoring agent
After=network-online.target

[Service]
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/.venv/bin/python -m opswatch_agent.cli --config $INSTALL_DIR/config.yaml
Restart=on-failure

[Install]
WantedBy=multi-user.target
UNIT

systemctl daemon-reload
systemctl enable --now opswatch-agent
echo "Installed. Edit $INSTALL_DIR/config.yaml, then: systemctl restart opswatch-agent"
