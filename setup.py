from distutils.core import setup

setup(
    name = 'ap',
    version="0.1",
    description = 'Syndication Aggretator',
    author = 'TWT Web Devs',
    author_email = 'webdev@washingtontimes.com',
    url = 'http://github.com/justquick/django-synagg',
    packages = ['synagg','synagg.management','synagg.management.commands'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ]
)
