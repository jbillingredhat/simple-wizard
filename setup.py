from setuptools import setup, find_packages

setup(
    name="simple-wizard",
    version="0.1.0",
    description="Scriptable Linux installation wizard with GTK4",
    author="",
    license="Apache-2.0",
    packages=find_packages(),
    install_requires=[
        "PyGObject>=3.42.0",
    ],
    entry_points={
        'console_scripts': [
            'simple-wizard=simple_wizard.wizard:main',
            'simple-wizard-client=simple_wizard.client:main',
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Installation/Setup",
    ],
)
