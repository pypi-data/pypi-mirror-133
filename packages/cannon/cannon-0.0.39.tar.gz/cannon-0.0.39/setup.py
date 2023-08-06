# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cannon']

package_data = \
{'': ['*']}

install_requires = \
['exscript==2.6.3', 'loguru==0.5.3', 'textfsm==1.1.2', 'traits==6.3.2']

setup_kwargs = {
    'name': 'cannon',
    'version': '0.0.39',
    'description': 'An SSH automation tool based on Exscript',
    'long_description': '# Introduction\n\ncannon is a wrapper around [exscript](https://pypi.python.org/pypi/exscript) to connect with remote server or network \ndevices with ssh.\n\n\n## Example Usage - Cisco IOS\n\nThis script will login, run a few show commands\n\n```python\nfrom cannon import Shell, Account\n\nsess = Shell(\n    host=\'route-views.routeviews.org\',\n    # route-views doesn\'t need password\n    account= Account(name=\'rviews\', password=\'\'),\n    debug=0,\n    )\n\nsess.execute(\'term len 0\')\n\n# relax_prompt reduces prompt matching to a minimum... relax_prompt is\n#     useful if the prompt may change while running a series of commands.\nsess.execute(\'show clock\')\n\nsess.execute(\'show version\')\nversion_text = sess.response\n\n# template is a TextFSM template\nvalues = sess.execute(\'show ip int brief\',\n    template="""Value INTF (\\S+)\\nValue IPADDR (\\S+)\\nValue STATUS (up|down|administratively down)\\nValue PROTO (up|down)\\n\\nStart\\n  ^${INTF}\\s+${IPADDR}\\s+\\w+\\s+\\w+\\s+${STATUS}\\s+${PROTO} -> Record""")\nprint("VALUES "+str(values))\nsess.close()\n```\n\n## Example Usage - Linux\n\n```python\nfrom getpass import getpass\n\nfrom cannon.main import Shell, Account\n\naccount = Account("mpenning", getpass("Login password: "))\nconn = Shell(host="127.0.0.1", port=22, account=account, driver="generic", debug=0)\nassert conn is not None\nexample_tfsm_template = """Value UNAME_LINE (.+)\n\nStart\n  ^${UNAME_LINE}\n"""\nprint(conn.execute("sudo uname -a", debug=0, template=example_tfsm_template, timeout=2))\nprint(conn.execute("whoami", debug=0, template=None, timeout=2))\n#print("FOO2", conn.response)\nconn.close(force=True)\n```\n\n## Example test suite setup\n\n- `git clone git@github.com:knipknap/Exscript`\n- `cd` into `Exscript/tests/Exscript/protocols` and `chmod 600 id_rsa`\n- exscript spawns a local tests ssh daemon, `pytest Exscript/tests/Exscript/protocols/SSH2Test.py`\n- Connect with `ssh -i id_rsa -p 1236 user@localhost`\n- one command is supported: `ls`\n\n\n.. _exscript: https://pypi.python.org/pypi/exscript\n',
    'author': 'Mike Pennington',
    'author_email': 'mike@pennington.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mpenning/cannon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
