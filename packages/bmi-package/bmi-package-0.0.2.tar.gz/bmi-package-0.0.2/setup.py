import setuptools

with open("README.md", "r") as fh:
    description = fh.read()

setuptools.setup(
    name="bmi-package",
    version="0.0.2",
    author="Saurabh Khare",
    author_email="saurabhkhare597@gmail.com",
    packages=["bmi_package"],
    description="BMI Calculation package",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/crypto597/code-20210109-saurabhkhare",
    license='MIT',
    python_requires='>=3.7',
    install_requires=[]
)