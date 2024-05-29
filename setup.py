import setuptools

setuptools.setup(
    name="jupyter_miircic_novnc_proxy",
    version='0.0.1',
    url="https://github.com/tiaden/jupyter-miircic-novnc-proxy",
    author="Edem Tiassou",
    description="Jupyter extension to proxy NoVnc",
    packages=setuptools.find_packages(),
	keywords=['Jupyter'],
	classifiers=['Framework :: Jupyter'],
    install_requires=[
        'jupyter-server-proxy>=3.2.3,!=4.0.0,!=4.1.0'
    ],
    entry_points={
        'jupyter_serverproxy_servers': [
            'miircic_novnc = jupyter_miircic_novnc_proxy:setup_vnc_server'
        ]
    },
    package_data={
        'jupyter_miircic_novnc_proxy': ['icons/novnc.svg'],
    },
)