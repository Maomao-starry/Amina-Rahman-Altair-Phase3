from setuptools import find_packages, setup

package_name = 'altair_phase3'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),
        (
            'share/' + package_name,
            ['package.xml']
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Amina Rahman',
    maintainer_email='aminarahmanshalu@gmail.com',
    description='ROS 2 rover telemetry and mission-control tasks',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'telemetry_pub = altair_phase3.mars_telemetry_publisher:main',
            'telemetry_monitor = altair_phase3.mission_control_monitor:main',
            'turtle_driving = altair_phase3.turtle_driving:main',
        ],
    },
)
