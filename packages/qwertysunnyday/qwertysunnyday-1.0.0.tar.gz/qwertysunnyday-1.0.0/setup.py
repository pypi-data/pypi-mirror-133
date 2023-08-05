from setuptools import setup
setup(
    name = 'qwertysunnyday',            #* Package will have this name
    packages = ['qwertysunnyday'],      #* name the package again. Why though?
    version = '1.0.0',                  #* To be increased every time we change library
    license='MIT',
    description = 'Weather forecast data',  # Short description of the library
    author = 'asdfasdf',                    #Author's name. Ardit in this case
    author_email = 'authorsemail@domain.com',
    url = 'https://domainname.com',     # Homepage of this library (github or whatever)
    keywords = ['qewrtyweather', 'qwertyforecast', 'qwertyopenweather'],  # Keywords users can search on pypi.org
    install_requires=['requests',],
    classifiers=[
        'Development Status :: 3 - Alpha',  # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)

