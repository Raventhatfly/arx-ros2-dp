from setuptools import find_packages, setup

package_name = 'dp_ros'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Feiyang Wu',
    maintainer_email='feiyangw.21@intl.zju.edu.cn',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'dp_inference = dp_ros.dp_inference:main',
            'pub_sub_test = dp_ros.pub_sub_test:main',
        ],
    },
)
