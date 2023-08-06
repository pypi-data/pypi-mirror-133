import os
from tmux_projector.utils import run_command

class Pane:
    def __init__(self, pane_name, window_name, session_name):
        self.pane_name = pane_name
        self.window_name = window_name
        self.session_name = session_name
        self.dir = None
        self.cmd = None
        self.venv = None

    def _load_config_from_json(self, pane_json):
        self.dir = pane_json.get('dir', None)
        self.cmd = pane_json.get('cmd', None)
        self.venv = pane_json.get('venv', None)

    def start(self):
        self._start_pane()
        if self.venv:
            venv_path = os.path.join(self.venv, 'bin/activate')
            self._send_keys(f'source Space "{venv_path}"')
        if self.dir:
            self._send_keys(f'cd Space "{self._format_command(self.dir)}" Enter')

        self._clean()

        if self.cmd:
            self._send_keys(f'"{self._format_command(self.cmd)}" Enter')


    
    def to_json(self):
        data = {'pane_name': self.pane_name, 'dir': self.dir, 'cmd': self.cmd, 'venv': self.venv}
        return data

    def _clean(self):
        self._send_keys(f"clear")

    def _format_command(self, cmd):
        # cmd = cmd.replace(" ", " Space ")
        return cmd

    def _start_pane(self):
        create_pane_command = f"tmux split-window -t {self.session_name}:{self.window_name}"
        run_command(create_pane_command)


    def _send_keys(self, cmd):
        # command = self._format_command(cmd)
        run_command(f"tmux send-keys -t {self.session_name}:{self.window_name}.{self.pane_name} {cmd} Enter")



