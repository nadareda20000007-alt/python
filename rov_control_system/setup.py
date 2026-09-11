import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'rov_control_system'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Installs all launch files into share/rov_control_system/launch/
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='nada',
    maintainer_email='nada@todo.todo',
    description='ROV control system package',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'joystick_node = rov_control_system.node.joystick_node:main',
            'navigation_node = rov_control_system.node.navigation_node:main',
        ],
    },
)