from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
        name="pyacmi",
        version='1.0.1',
        description="ACMI flight record file parser",
        long_description=long_description,
        long_description_content_type='text/markdown',
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
