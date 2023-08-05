# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['event_horyzen']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'h5py>=3.6.0,<4.0.0',
 'ipython>=7.30.1,<8.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.21.5,<2.0.0',
 'scipy>=1.7.3,<2.0.0']

extras_require = \
{'pyqt': ['pyqtgraph>=0.12.3,<0.13.0',
          'PyOpenGL>=3.1.5,<4.0.0',
          'PyQt5>=5.15.6,<6.0.0']}

entry_points = \
{'console_scripts': ['event-horyzen = event_horyzen.event_horyzen:cli',
                     'event-horyzen-plot = event_horyzen.animated_plot:cli']}

setup_kwargs = {
    'name': 'event-horyzen',
    'version': '0.1.0',
    'description': 'Simulates geodesic motion around black holes.',
    'long_description': '#+TITLE: Event hoRyzen\n*Event hoRyzen* is a Python library designed to simulate and visualize geodesic motion around Schwarzschild, Reisner-Nordstrom, Kerr, and Kerr-Newman black holes.\nIt uses a slightly modified version of Pierre Christian and Chi-kwan Chan\'s FANTASY geodesic integration code (see https://github.com/pierrechristian/FANTASY + Pierre Christian and Chi-kwan Chan 2021 /ApJ/ *909* 67).\n\n* Installation\n** pip\n#+begin_src bash :eval never\npip install event_horyzen\n#+end_src\n\n*or*\n#+begin_src bash  :eval never\npip install event_horzyen[pyqt]\n#+end_src\n\nDepending on whether or not you\'d like to use the =pyqtgraph= and =opengl= plotting modules (They are not small dependencies. The option to plot with matplotlib is included in the base package).\n** Manually\n#+begin_src bash :eval never\ngit clone https://github.com/UCF-SPS-Research-21/research-proj21\n#+end_src\n\nIf you use Poetry for package and venv management, you can use\n#+begin_src bash :eval never\npoetry install event_horyzen\n#+end_src\n\n*or*\n#+begin_src bash  :eval never\npoetry install event_horzyen[pyqt]\n#+end_src\n\nIf you don\'t, you can =pip install -r requirements.txt= or =conda install --file requirements.txt=.\nThere are multiple versions of requirements.txt provided, it should be evident what each is for.\n\n* Usage\nThe code is configured with a YAML configuration file.\nPlease see the example at [[file:event_horyzen/config.yml]]\n\n** Example\n*I use Unix paths in the examples. Windows paths will work too*\n\nIf you\'d like to use the default configuration, you can just leave the argument to =event_horyzen.run()= empty.\nTo copy the default config and edit it, do the following.\n\n#+begin_src python :eval never\nfrom pathlib import Path\nfrom event_horyzen import event_horyzen\n\ndest = Path("./foo/")\nevent_horyzen.copy_default_config(dest)\n#+end_src\n\nIf you don\'t specify a destination, it will copy the file to your current working directory.\nNow, assuming you\'ve edited the config to your liking and its named =config.yml=:\n\n#+begin_src python :eval never\nfrom pathlib import Path\nfrom event_horyzen import event_horyzen\n\nconf_path = Path(\'./config.yml\')\nevent_horyzen.run(conf_path)\n#+end_src\n\n*or for multiple geodesics simulated in parallel*\n\n#+begin_src python :eval never\nfrom pathlib import Path\nfrom event_horyzen import event_horyzen\n\nconf_path1 = Path(\'./config1.yml\')\nconf_path2 = Path(\'./config2.yml\')\nconf_path3 = Path(\'./config3.yml\')\n\nconfs = [conf_path1, conf_path2, conf_path3]\n\nevent_horyzen.run(confs)\n#+end_src\n\n\n\nA unique directory under the output directory specified in the configuration file will be created in the format =<output-dir>/<date+time>_<name-of-config-file>=.\nSo, it makes sense to give your configuration files meaningful names.\nThe geodesic in both spherical and cartesian coordinates will be saved to this directory as =results.h5=.\nThe configuration file used to generate the simulation will be copied to this directory as well to ensure reproducibility.\nA basic plot of the geodesic is also created and saved in the directory as both a .PNG and a =pickle= file so that the figure can be reloaded and interacted with.\n[[./example-kerr-newman.png][Example Kerr-Newman Plot]]\n\nFor the 3D plotting,\n#+begin_src python :eval never\nfrom pathlib import Path\nfrom event_horyzen import animated3Dplot as a3d\n\nresults = Path("./results.h5")\nviz = a3d.Visualizer(results)\nviz.animation()\n#+end_src\n\n*or for multiple geodesics on the same plot*\n\n#+begin_src python :eval never\nfrom pathlib import Path\nfrom event_horyzen import animated3Dplot as a3d\n\nresults1 = Path("./results1.h5")\nresults2 = Path("./results2.h5")\nresults3 = Path("./results3.h5")\n\nresults = [results1, results2, results3]\n\nviz = a3d.Visualizer(results)\nviz.animation()\n#+end_src\n\n\nBy default, it puts a photon sphere for a M=1 (geometrized units) schwarzschild black hole on the plot for reference.\nThis can be turned off or modified in the call to =Visualizer()=.\n',
    'author': 'David Wright',
    'author_email': 'davecwright@knights.ucf.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/UCF-SPS-Research-21/event-horyzen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
