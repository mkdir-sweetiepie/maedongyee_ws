from setuptools import setup

package_name = 'aicar_driver'

setup(
    name=package_name,
    version='0.2.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='medong',
    maintainer_email='medong@kw.ac.kr',
    description='Motor driver',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'differential_drive_node = aicar_driver.differential_drive_node:main',
        ],
    },
)
