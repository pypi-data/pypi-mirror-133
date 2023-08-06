import setuptools

setuptools.setup(
    name='dowgo',
    version='1.0.2',
    scripts=['dowgo/dowgo'],
    author="NDRAEY",
    description="Just a simple package manager",
    long_description=open("README.txt").read(),
    packages=setuptools.find_packages()
)
