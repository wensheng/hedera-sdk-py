import os
import setuptools

src_files = os.listdir("src/hedera")
jar_file = [a for a in src_files if a.startswith("sdk-") and a.endswith("-uber.jar")]
if not jar_file:
    exit("jar file must exist before packaging")
jar_file = jar_file[0]
version = jar_file[4:-9]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hedera-sdk-py", # Replace with your own username
    version=version,
    author="Wensheng Wang",
    author_email="wenshengwang@gmail.com",
    description="Hedera SDK in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wensheng/hedera-sdk-py",
    project_urls={
        "Bug Tracker": "https://github.com/wensheng/hedera-sdk-py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=['pyjnius>=1.3.0'],
    python_requires=">=3.6",
    include_package_data=True,
    package_data={ "hedera": ["*.jar"]},
)
