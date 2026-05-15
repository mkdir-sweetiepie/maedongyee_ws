import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'aicar_vision'

setup(
    name=package_name,
    version='0.2.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'calibration_data'),
            glob(os.path.join('calibration_data', '*.p'))),
        (os.path.join('share', package_name, 'models'),
            glob(os.path.join('models', '*.tflite'))),
    ],
    install_requires=['setuptools', 'numpy'],
    zip_safe=True,
    maintainer='medong',
    maintainer_email='medong@kw.ac.kr',
    description='Lane detection (BEV + polyfit) and sign detection',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'lane_detector_node = aicar_vision.lane_detector_node:main',
            'sign_detector_node = aicar_vision.sign_detector_node:main',
            'fake_detector_node = aicar_vision.fake_detector_node:main',
        ],
    },
)
