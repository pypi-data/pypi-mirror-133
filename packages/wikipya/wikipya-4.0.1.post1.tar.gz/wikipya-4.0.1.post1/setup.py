# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wikipya', 'wikipya.methods', 'wikipya.models']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0',
 'httpx>=0.21.2,<0.22.0',
 'pydantic>=1.9.0,<2.0.0',
 'tghtml>=1.0.6,<2.0.0']

setup_kwargs = {
    'name': 'wikipya',
    'version': '4.0.1.post1',
    'description': 'A simple async python library for search pages and images in wikis',
    'long_description': '<div align="center">\n  <h1>📚 wikipya</h1>\n  <h3>A simple async python library for search pages and images in wikis</h3>\n</div><br>\n\n## 🛠 Usage\n```python\n# Import wikipya\nfrom wikipya import Wikipya\n\n# Create Wikipya object with Wikipedia methods\nwiki = Wikipya(lang="en").get_instance()\n\n# or use other MediaEiki server (or other service, but this is\'n fully supported now)\n\nwikipya = Wikipya(url="https://ipv6.lurkmo.re/api.php", lurk=True, prefix="").get_instance()\n\n# for use Lurkmore (russian). simple and fast\n\n# Get a pages list from search\nsearch = await wiki.search("test")\n\n# Get a pages list from opensearch\nopensearch = await wiki.opensearch("test")\n\n# Get page class\n# You can give to wiki.page() search item, title of page, page id\n\n# Search item (supported ONLY by wiki.search)\npage = await wiki.page(search[0])\n\n# Page title\npage = await wiki.page("git")\n\n# Pageid\npage = await wiki.page(800543)\n\nprint(page.html)       # Get page html\nprint(page.parsed)     # Get html cleared of link, and other non-formating tags\n\n# Get image\nimage = await wiki.image(page.title)  # may not work in non-wikipedia services, check true prefix, or create issue\n\nprint(image.source)    # Image url\nprint(image.width)     # Image width\nprint(image.height)    # Image height\n```\n\n## 🎉 Features\n- Full async\n- Support of other instances of MediaWiki\n- Support cleaning of HTML with TgHTML\n- Uses models by [pydantic](https://github.com/samuelcolvin/pydantic)\n\n## 🚀 Install\nTo install, run this code:\n```\npip install wikipya\n```\n',
    'author': 'Daniel Zakharov',
    'author_email': 'daniel734@bk.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
