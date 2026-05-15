from setuptools import find_packages, setup

package_name = 'aicar_ui'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'numpy', 'Pillow'],
    zip_safe=True,
    maintainer='medong',
    maintainer_email='medong@kw.ac.kr',
    description='Local Tkinter dashboard for AI car',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'dashboard_node = aicar_ui.dashboard_node:main',
        ],
    },
)
