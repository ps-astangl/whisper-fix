from setuptools import setup, find_packages

setup(
    name='whisper-fix',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],  # Dependencies are handled in install.py
    entry_points={
        'console_scripts': [
            'whisper-fix=whisper_fix.main:cli',
        ],
    },
    author='AJ Stangl',
    author_email='ajstangl@bruh.biz',
    description='A tool for TTS and grammar correction using Whisper and LLM',
    url='https://github.com/ajstangl/whisper-fix',
)

