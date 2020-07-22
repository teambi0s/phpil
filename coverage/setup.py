from distutils.core import setup, Extension

module1 = Extension('phpcov',
                    define_macros = [('MAJOR_VERSION', '1'),
                                     ('MINOR_VERSION', '0')],
                    include_dirs = ['/usr/local/include'],
                    # libraries = ['tcl83'],
                    library_dirs = ['/usr/local/lib'],
                    sources = ['./phpcov.c'])

setup (name = 'phpcov',
       version = '1.0',
       description = 'Package to obtain code coverage',
       author = 'Vignesh S Rao',
       author_email = 'vigneshsrao5@gmail.com',
       url = 'https://docs.python.org/extending/building',
       long_description = '''
This is really just a demo package.
''',
       ext_modules = [module1])
