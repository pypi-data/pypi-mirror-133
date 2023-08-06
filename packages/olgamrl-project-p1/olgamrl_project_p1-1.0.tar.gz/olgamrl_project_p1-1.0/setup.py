import setuptools, os
setuptools.setup(
    name="olgamrl_project_p1",  # Replace with your own PyPi
    version="1.0",
    author="Foo Bar",
    author_email="lidor.ettinger@example.com",
    description="A small example package",
    url="https://github.com/naturalett/getting-started",
    install_requires=['distribution-Final'],
    packages=['calculator'],
    scripts=['calculator/calc.py'],
    python_requires='>=3.9',
)
