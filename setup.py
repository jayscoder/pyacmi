from setuptools import setup

setup(
        name="pyacmi",
        version='1.0.0',
        description="ACMI flight record file parser",
        long_description="ACMI is a file used by tacview for creating flight recording from simulators or real world.",
        url='https://github.com/wangtong2015/pyacmi',
        author="Wang Tong",
        author_email="astroboythu@gmail.com",
        license="MIT",
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Topic :: Games/Entertainment :: Simulation',
            'Intended Audience :: Developers',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3 :: Only'
        ],
        keywords='acmi tacview',
        install_requires=['sortedcontainers'],
        packages=['pyacmi'],
)
