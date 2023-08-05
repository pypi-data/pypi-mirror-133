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
    'version': '0.1.2',
    'description': 'Simulates geodesic motion around black holes.',
    'long_description': '\n# Table of Contents\n\n1.  [Installation](#org9526257)\n    1.  [pip](#org8d3b001)\n    2.  [Manually](#org49b83bc)\n2.  [Usage](#org8d40f3c)\n    1.  [Example](#orgb8fd713)\n\n**Event hoRyzen** is a Python library designed to simulate and visualize geodesic motion around Schwarzschild, Reisner-Nordstrom, Kerr, and Kerr-Newman black holes.\nIt uses a slightly modified version of Pierre Christian and Chi-kwan Chan&rsquo;s FANTASY geodesic integration code (see <https://github.com/pierrechristian/FANTASY> + Pierre Christian and Chi-kwan Chan 2021 *ApJ* **909** 67).\n\n\n<a id="org9526257"></a>\n\n# Installation\n\n\n<a id="org8d3b001"></a>\n\n## pip\n\n    pip install event-horyzen\n\n**or**\n\n    pip install event-horzyen[pyqt]\n\n(If you use `zsh` as your shell you will need to quote the package name for optional dependencies, i.e., &ldquo;event-horyzen[pyqt]&rdquo;)\n\nDepending on whether or not you&rsquo;d like to use the `pyqtgraph` and `opengl` plotting modules (They are not small dependencies. The option to plot with matplotlib is included in the base package).\n\n\n<a id="org49b83bc"></a>\n\n## Manually\n\n    git clone https://github.com/UCF-SPS-Research-21/event-horyzen\n\nIf you use Poetry for package and venv management, you can use\n\n    poetry install\n\n**or**\n\n    poetry install -E pyqt\n\nIf you don&rsquo;t, you can `pip install -r requirements.txt` or `conda install --file requirements.txt`.\nThere are multiple versions of requirements.txt provided, it should be evident what each is for.\n\n\n<a id="org8d40f3c"></a>\n\n# Usage\n\nThe code is configured with a YAML configuration file.\nPlease see the example at <event_horyzen/config.yml>\n\n\n<a id="orgb8fd713"></a>\n\n## Example\n\n**I use Unix paths in the examples. Windows paths will work too &#x2014; just make sure you escape backslashes or make use of `pathlib`&rsquo;s functionality.**\n\nIf you&rsquo;d like to use the default configuration, you can just leave the argument to `event_horyzen.run()` empty.\nTo copy the default config and edit it, do the following.\n\n    from pathlib import Path\n    from event_horyzen import event_horyzen\n    \n    dest = Path("./foo/")\n    event_horyzen.copy_default_config(dest)\n\nIf you don&rsquo;t specify a destination, it will copy the file to your current working directory.\nNow, assuming you&rsquo;ve edited the config to your liking and its named `config.yml`:\n\n    from pathlib import Path\n    from event_horyzen import event_horyzen\n    \n    conf_path = Path(\'./config.yml\')\n    event_horyzen.run(conf_path)\n\n**or for multiple geodesics simulated in parallel**\n\n    from pathlib import Path\n    from event_horyzen import event_horyzen\n    \n    conf_path1 = Path(\'./config1.yml\')\n    conf_path2 = Path(\'./config2.yml\')\n    conf_path3 = Path(\'./config3.yml\')\n    \n    confs = [conf_path1, conf_path2, conf_path3]\n    \n    event_horyzen.run(confs)\n\nA unique directory under the output directory specified in the configuration file will be created in the format `<output-dir>/<date+time>_<name-of-config-file>`.\nSo, it makes sense to give your configuration files meaningful names.\nThe geodesic in both spherical and cartesian coordinates will be saved to this directory as `results.h5`.\nThe configuration file used to generate the simulation will be copied to this directory as well to ensure reproducibility.\nA basic plot of the geodesic is also created and saved in the directory as both a .PNG and a `pickle` file so that the figure can be reloaded and interacted with.\n[Example Kerr-Newman Plot](./example-kerr-newman.png)\n\nIf you want to load the pickled Matplotlib plot, you can do the following.\n\n    import pickle as pl\n    from pathlib import Path\n    \n    plot_path = Path("<path-to-plot>/basic-plot.pickle")\n    \n    with open(plot_path, "rb") as plot:\n        fig = pl.load(plot)\n    \n    # Now do whatever you want with the figure!\n    \n    fig.show()\n\nFor the 3D plotting,\n\n    from pathlib import Path\n    from event_horyzen import animated_plot as ap\n    \n    results = Path("./results.h5")\n    viz = ap.Visualizer(results)\n    viz.animation()\n\n**or for multiple geodesics on the same plot**\n\n    from pathlib import Path\n    from event_horyzen import animated_plot as ap\n    \n    results1 = Path("./results1.h5")\n    results2 = Path("./results2.h5")\n    results3 = Path("./results3.h5")\n    \n    results = [results1, results2, results3]\n    \n    viz = ap.Visualizer(results)\n    viz.animation()\n\nBy default, it puts a photon sphere for a M=1 (geometrized units) schwarzschild black hole on the plot for reference.\nThis can be turned off or modified in the call to `Visualizer()`.\n\n**Both the simulation and the plotting can be ran directly from the command line**\n\nFirst, the simulation tools.\n\n    event-horyzen -h\n\n    usage: event-horyzen [-h] [datapath ...]\n    \n    positional arguments:\n      datapath    The path(s) to the configuration file(s). Defaults to the\n                  included `config.yml` if not provided.\n    \n    options:\n      -h, --help  show this help message and exit\n\nNow, the plotting tools.\n\n    event-horyzen-plot -h\n\n    usage: event-horyzen-plot [-h] datapath [datapath ...]\n    \n    positional arguments:\n      datapath    The path(s) to the data file(s).\n    \n    options:\n      -h, --help  show this help message and exit\n\n',
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
