from setuptools import setup
from setuptools import Distribution
import pyang


class PyangTestDist(Distribution):
    """The purpose of this subclass of Distribution is to extend the
      install procedure with preprocessing of shell scripts and man
      pages so that they reflect the actual installation prefix, which
      may be changed through the --prefix option.
      """

    def preprocess_files(self, prefix):
        """Change the installation prefix where necessary.
            """
        if prefix is None: return

    def run_commands(self):
        opts = self.command_options
        if "install" in opts:
            self.preprocess_files(opts["install"].get("prefix",
                                                      ("", None))[1])
        Distribution.run_commands(self)


script_files = []

setup(name='pyang-test',
      version=pyang.__version__,
      author='stonearest',
      author_email='sgq0859@163.com',
      description="B",
      long_description="A",
      url='https://github.com/stonearest/pyang-test',
      install_requires=["pyang>=2.5.2", "pyangbind>=0.8.1"],
      license='BSD',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
      ],
      keywords='YANG Test Tools',
      distclass=PyangTestDist,
      scripts=script_files,
      packages=[],
      data_files=[]
)