# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bobcat_miner']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=1.11.1,<2.0.0', 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'bobcat-miner',
    'version': '0.2.0',
    'description': 'A python SDK for interacting with the bobcat miner.',
    'long_description': '# bobcat-miner-python\n\nA python SDK for interacting with the bobcat miner.\n\n# Install\n\n```bash\npip install bobcat-miner-python\n```\n\n# Bobcat Usage\n\n```python\nimport bobcat_miner\n\nbobcat = Bobcat(ip_address="192.168.1.10")\n\n# data refresh\nbobcat.refresh_status()\nprint(bobcat.status)\n# {"status": "Synced", "gap": "0", "miner_height": "1148539", "blockchain_height": "1148539", "epoch": "30157"}\n\nbobcat.refresh_miner()\nprint(bobcat.miner)\n# {"ota_version": "1.0.2.66", "region": "region_us915", "frequency_plan": "us915", "animal": "my-mocked-miner", ... }\n\nbobcat.refresh_speed()\nprint(bobcat.speed)\n# {"DownloadSpeed": "94 Mbit/s", "UploadSpeed": "57 Mbit/s", "Latency": "7.669083ms"}\n\nbobcat.refresh_dig()\nprint(bobcat.dig)\n# {"name": "seed.helium.io.", "DNS": "Local DNS", "records": [{"A": "54.232.171.76", ... ]}\n\n# actions\nbobcat.reboot()\nbobcat.resync()\nbobcat.fastsync()\nbobcat.reset()\n\n# diagnostics\nbobcat.is_healthy()\nbobcat.is_running()\nbobcat.is_synced()\nbobcat.is_temp_safe()\nbobcat.has_errors()\nbobcat.is_relayed()\nbobcat.should_reboot())\nbobcat.should_resync()\nbobcat.should_fastsync()\nbobcat.should_reset()\n```\n\n:warning: `bobcat.refresh_speed()` takes about 30 seconds to complete and you should not call it repeatedly. Doing so will slow down your internet speed, which in turn will slow down your miner.\n\n# Autopilot Usage\n\nIf the bobcat miner is unhealthy then the autopilot will attempt to repair it.\n\n```python\nimport os\n\nimport bobcat\n\nbobcat = Bobcat(os.getenv("BOBCAT_IP_ADDRESS"))\nbobcat.autopilot()\n```\n\n# Troubleshooting\n\nPlease see [No Witness\'s Troubleshooting Guide](https://www.nowitness.org/troubleshooting/) for more information troubleshooting your bobcat miner.\n\n# Donations\n\nDonations are welcome and appreciated!\n\n[![HNT: 14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR](./images/wallet.jpg)](https://explorer-v1.helium.com/accounts/14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR)\n\nHNT: [14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR](https://explorer-v1.helium.com/accounts/14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR)\n',
    'author': 'Aidan Melen',
    'author_email': 'aidanmelen@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aidanmelen/bobcat-miner-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
