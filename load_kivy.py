# Version 2020.11

import subprocess
import sys

def install(packages):
	subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-cache-dir"] + packages)

def uninstall_deps():
	subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", "kivy.deps.glew", "kivy.deps.gstreamer", "kivy.deps.sdl2", "kivy.deps.angle"])

def update_pip():
	if sys.platform.startswith("linux"):
		install(["--upgrade", "--user", "pip", "setuptools", "virtualenv"])
	elif sys.platform == "win32":
		install(["--upgrade", "pip", "wheel", "setuptools", "virtualenv"])

def install_deps():
	install(['PyHamcrest'])
	if sys.platform == "win32":
		install(['docutils', 'pygments', 'pypiwin32', 'kivy.deps.sdl2==0.1.*', 'kivy.deps.glew==0.1.*'])
	

def install_kivy():
	if sys.platform == "darwin":
		install(['kivy'])
	if sys.platform.startswith("linux"):
		install(['kivy'])
	if sys.platform == "win32":
		install(['kivy==1.11.1'])

if __name__ == "__main__":
	is_64bits = sys.maxsize > 2**32
	if not (is_64bits and sys.version_info.major == 3 and (sys.version_info.minor >= 5 or sys.version_info.minor <= 7)):
		print("Installez la version 3.7(64 bits) de Python ou selectionnez la en cliquant sur le numéro de version dans le coin inférieur gauche.")
		sys.exit(0)
	uninstall_deps()
	#update_pip()
	install_deps()
	install_kivy()