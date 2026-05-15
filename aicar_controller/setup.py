from setuptools import setup

package_name = 'aicar_controller'

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
    description='Driving controller',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'driving_controller_node = aicar_controller.driving_controller_node:main',
        ],
    },
)
