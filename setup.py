from setuptools import setup, find_packages
import os, json

def get_info():
	setup_path = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
	_info_json_path = os.path.join(setup_path, "web2pdf", "_info.json")
	with open(_info_json_path) as jfile:
		jdata = json.load(jfile)
	return jdata

data = get_info()
setup(
    name=data["name"],
    version=data["version"],
    description=data["desc"],
    author=data["author"],
    keywords=data["keywords"],
    project_urls=data["project_urls"],
    packages=find_packages(),
    install_requires=data["dependencies"],
    include_package_data=True,
    package_data={
        '_info': [os.path.join('web2pdf', '_info.json')]
    }
)
