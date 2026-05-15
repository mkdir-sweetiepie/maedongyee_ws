import os
from glob import glob
from setuptools import setup

package_name = 'aicar_vision'

setup(
    name=package_name,
    version='0.2.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'calibration_data'),
            glob(os.path.join('calibration_data', '*.p'))),
        (os.path.join('share', package_name, 'models'),
            glob(os.path.join('models', '*.tflite'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='medong',
    maintainer_email='medong@kw.ac.kr',
    description='Lane and sign detection',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'lane_detector_node = aicar_vision.lane_detector_node:main',
            'sign_detector_node = aicar_vision.sign_detector_node:main',
            'fake_detector_node = aicar_vision.fake_detector_node:main',
        ],
    },
)
