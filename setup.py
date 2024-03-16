from setuptools import setup, find_packages

setup(
    name="riscv_cocotb",
    version="0.1.3",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "riscv_cocotb": ["dis.sh"],
    },
    author="Eymen Ünay",
    author_email="eymenunay@outlook.com",
    description="A test generator for RISC-V based on Cocotb",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/eymay/riscv-cocotb",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
    install_requires=[
        'cocotb',
        'riscv-assembler',
        'pytest',
        # 'functools'
    ],
)

