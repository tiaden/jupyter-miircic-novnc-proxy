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


def _novnc_urlparams():
    url_params = ('?video_quality=2' +
    '&enable_webp=false' +
    '&autoconnect=1' +
    '&path=miircic_vnc/websockify' +
    '&cursor=true' +
    '&resize=remote' +
    '&clipboard_up=true'
    '&clipboard_down=true'
    '&clipboard_seamless=true'
    '&toggle_control_panel=null')

    return url_params


def _novnc_mappath(path):
    # always pass the url parameter
    if path in ('/', '/vnc.html',):
        url_params = _novnc_urlparams()
        path = '/vnc.html' + url_params

    return path


def setup_vnc_server():
    def _get_env(port):
        return dict(NO_VNC_PORT=str(port))

    def _get_cmd():
        cmd = [
            get_vnc_server_script('vnc_startup.sh'),
        ]

        return cmd

    path_info = 'miircic_vnc/vnc.html' + _novnc_urlparams()

    server_process = {
        'command': _get_cmd,
        'timeout': 90,
        'mappath': _novnc_mappath,
        'absolute_url': False,
        'new_browser_tab': True,
        'environment': _get_env,
        'launcher_entry': {
            'enabled': True,
            'title': 'MiircicVNC',
            'icon_path': get_icon_path(),
            'path_info': path_info,
        }
    }
    return server_process
