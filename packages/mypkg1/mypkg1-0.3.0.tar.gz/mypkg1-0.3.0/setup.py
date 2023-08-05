import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command


here = os.path.abspath(os.path.dirname(__file__))

# Package Meta-Data
NAME = 'mypkg1'  # 模块名称
VERSION = '0.3.0'  # major.minor[.patch][sub]  主版本.次版本.补丁[子补丁]
AUTHOR = 'MY'  # 作者
AUTHOR_EMAIL = 'my@example.com'  # 作者邮箱
MAINTAINER = AUTHOR  # 维护者
MAINTAINER_EMAIL = AUTHOR_EMAIL  # 维护者邮箱
URL = 'https://github.com/my/pkg1'  # 模块主页
DOWNLOAD_URL = URL  # 模块下载地址
REQUIRES_PYTHON = '>=3.7'
REQUIRED = ['requests', 'tqdm']
EXTRAS = {}
DESCRIPTION = 'This is MyPkg-1.'
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8-sig') as what:
        LONG_DESCRIPTION = '\n' + what.read()
except FileNotFoundError:
    LONG_DESCRIPTION = DESCRIPTION


class ModuleCommand(Command):

    description = 'Module Self Command.'
    user_options = []

    @staticmethod
    def status(text):
        print(f"\033[1m{text}\033[0m")

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds...')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        # os.system('python setup.py sdist bdist_wheel --universal')
        os.system('python setup.py install')

setup(
    name=NAME,  # 作者
    version=VERSION,  # 版本
    description=DESCRIPTION,  # 概述
    long_description=LONG_DESCRIPTION,  # 详细描述
    long_description_content_type='text/markdown',  # 详细描述文档类型，一般为md
    author=AUTHOR,  # 作者
    author_email=AUTHOR_EMAIL,  # 作者邮箱
    maintainer=MAINTAINER,  # 维护者
    maintainer_email=MAINTAINER_EMAIL,  # 维护者邮箱
    url=URL,

    python_requires=REQUIRES_PYTHON,

    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    # py_modules=['mypackage'],  # 单个模块直接指定模块名称
    # package_data={'': ['LICENSE', 'NOTICE']},  # 模块扩展数据
    # package_dir={'requests': 'requests'},  #

    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: Freeware',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet',
    ],
    # $ setup.py publish support.
    cmdclass={
        'module': ModuleCommand,
    },
    keywords = ['test', 'package']
)


print('感谢您的使用，祝您投资顺利。')
print('Thank you for your use, wish you a successful investment.')