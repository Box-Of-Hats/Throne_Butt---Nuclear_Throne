from cx_Freeze import setup, Executable

setup(name='ThroneButt',
	version='1.2',
	description='View Throne Butt Scores',
	executables = [Executable("thronebutt.py")])