import os
import shutil


def get_vnc_server_script(prog):
    other_paths = [
        os.path.join('/dockerstartup', prog),
    ]
    if shutil.which(prog):
        return prog

    for op in other_paths:
        if os.path.exists(op):
            return op

    raise FileNotFoundError(f'Could not find {prog} in PATH')


def get_icon_path():
    if os.getenv('NOVNC_PROXY_ICON_URL'):
        return os.getenv('NOVNC_PROXY_ICON_URL')
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'icons', 'novnc.svg'
    )


def setup_vnc_server():
    def _get_env(port):
        return dict(NO_VNC_PORT=str(port))

    def _get_cmd():
        cmd = [
            get_vnc_server_script('vnc_startup.sh'),
        ]

        return cmd

    server_process = {
        'command': _get_cmd,
        'timeout': 90,
        'environment': _get_env,
        'launcher_entry': {
            'title': 'MiircicVNC',
            'icon_path': get_icon_path()
        }
    }
    return server_process
