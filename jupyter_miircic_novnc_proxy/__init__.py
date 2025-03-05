import os
import shutil
import logging

logger = logging.getLogger(__name__)
logger.setLevel('INFO')


def get_vnc_server_script(prog):
    other_paths = [
        os.path.join(os.getenv('STARTUPDIR','/startup'), prog),
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
        os.path.dirname(os.path.abspath(__file__)), 'icons', 'novnc-new.svg'
    )


# def _novnc_urlparams():
#     url_params = ('?video_quality=3'
#                   '&enable_webp=false'
#                   '&autoconnect=1'
#                   '&path=miircic-vn/websockify'
#                   '&idle_disconnect=20'
#                   '&cursor=true'
#                   '&resize=remote'
#                   '&clipboard_up=true'
#                   '&clipboard_down=true'
#                   '&clipboard_seamless=true'
#                   '&toggle_control_panel=false')
#
#     return url_params
#
#
# def _novnc_mappath(path):
#     logger.info('Before path transform: ' + path)
#     # always pass the url parameter
#     if path in ('/', '/index.html', '/vnc.html'):
#         path = '/vnc.html' + _novnc_urlparams()
#     logger.info('After path transform: ' + path)
#
#     return path


def _novnc_response(path, host, response, orig_response, port):
    # Add server header in case of Lossless mode
    response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    response.headers["Cross-Origin-Resource-Policy"] = "same-site"


def setup_vnc_server():
    #def _get_env(port):
    #    return dict(NO_VNC_PORT="6901")

    def _get_cmd():
        cmd = [
            get_vnc_server_script('vnc_startup.sh'),
        ]

        return cmd

    server_process = {
        'command': _get_cmd,
        'timeout': 90,
        "rewrite_response": _novnc_response,
        'absolute_url': False,
        'port': 6901,
        'new_browser_tab': True,
        #        'environment': _get_env,
        'launcher_entry': {
            'enabled': True,
            'title': os.getenv('NOVNC_PROXY_TITLE', 'Miircic VNC'),
            'icon_path': get_icon_path(),
        }
    }
    return server_process
