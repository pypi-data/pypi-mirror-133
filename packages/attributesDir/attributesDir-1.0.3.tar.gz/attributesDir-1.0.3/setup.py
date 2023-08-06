from setuptools import setup, find_packages
from attributesDir.attributesDir import __package__, __author__, __email__, __version__, __url__, __license__

setup(
    name=__package__,
    version=__version__,
    keywords=(["dir", "dir_object", "classify", "modules",
               "function_or_method", "class", "functions",
               "methods", "constants", "format_dir"]),
    description="""change type(attribute).__name__ == 'methos' to 'method' and delete entry_points in setup function""",
    long_description="""Print and return an alphabetized list of names, which
    have a number and background color if print them, comprising (some of)
    the attributes of the given object, and of attributes reachable from it.
    """,
    # metadata for upload to PyPI
    license=__license__,
    url=__url__,
    author=__author__,
    author_email=__email__,

    packages=find_packages(), # ['mypackage']
    include_package_data=True,
    platforms="any",
    python_requires='>=3.6',  # 安装环境的限制
    install_requires=[],  # 表明当前模块依赖哪些包，若环境中没有，则会从pypi中下载安装
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)


