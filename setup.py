from distutils.core import setup


def readme():
    """Import the README.md Markdown file and try to convert it to RST format."""
    try:
        import pypandoc
        return pypandoc.convert('README.md', 'rst')
    except(IOError, ImportError):
        with open('README.md') as readme_file:
            return readme_file.read()


setup(
    name='my_package',
    version='0.1',
    description='Reinforcement Learning from Jannik Zürn Medium Blog',
    long_description=readme(),
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    # Substitute <github_account> with the name of your GitHub account
    url='https://github.com/vutgithub/reinforcement_learning_jannik_zurn',
    author='Thanh Vu',  # Substitute your name
    author_email='tvu@xebia.fr',  # Substitute your email
    license='Xebia',
    packages=['my_package'],
    install_requires=[
        'pypandoc>=1.4',
    ],
)
