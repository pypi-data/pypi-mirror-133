import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    version='0.1.1',
    author='redj_ai',
    name='Redj Captcha',
    url='https://redj.ai/',
    description='Redj Captcha',
    author_email='info@redj.ai',
    long_description=long_description,
    install_requires=['Pillow==9.0.0', 'django'],
    long_description_content_type="text/markdown",
    project_urls={
        "Bug Tracker": "https://redj.ai/",
    },
    classifiers=[
        'Framework :: Django',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires=">=3",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)
