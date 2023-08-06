from setuptools import setup

with open("README.md", "r") as f:
  long_description = f.read()

setup(name='relativeimport',  # 包名
      version='99.0.6',  # 版本号
      description='do shorter code to import from relative path',
      long_description=long_description,
      author='ltaoist',
      author_email='ltaoist@163.com.com',
      install_requires=[],
      license='BSD License',
      package_dir={"relativeimport":"pkg"},
      packages=["relativeimport"],
      long_description_content_type="text/markdown",
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python'
      ],
      )
