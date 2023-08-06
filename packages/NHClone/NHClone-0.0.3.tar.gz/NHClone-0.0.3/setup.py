from setuptools import setup, find_packages
import os

with open("README.md", "r") as fh:
    long_description = fh.read()






setup(
    name='NHClone',
    packages=find_packages(),
    include_package_data=True,
    version="0.0.3",
    description='Facebook Old Id Cloning Tool For All',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Md Nayem Sheikh',
    author_email='nayeme19@gmail.com',
    install_requires=['lolcat','requests','mechanize'],
    
    
    keywords=['fb old id clone ', 'facebook Old id clone', 'noob71', 'noob-hacker', 'Noob-Hcaker71 tool',
                  'Noob-Hcaker71', 'bomb sms', 'termux hack', 'noob hack', 'Noob tool'],
    classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Operating System :: OS Independent',
            'Environment :: Console',
    ],
    
    license='MIT',
    entry_points={
            'console_scripts': [
                'NH-Clone = NHClone.Noob:menu',
                
            ],
    },
    python_requires='>=2.7.18'
)