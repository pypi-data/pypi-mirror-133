from importlib.machinery import SourceFileLoader
import os.path
import sys

class _module:

    def __call__(self, file, path, mod_name=None):
        dirpath = os.path.dirname(file)
        impath = os.path.abspath(os.path.join(dirpath, path))
        if mod_name is None:
            mod_name = os.path.basename(impath)
            mod_name = os.path.splitext(mod_name)[0]
        if not impath.endswith('.py'):
            a = os.path.join(impath, '__init__.py')
            if os.path.exists(a):
                impath = a
            else:
                b = "%s.py" % impath
                if os.path.exists(b):
                    impath = b
                else:
                    raise ImportError("relativeimport do do understand %s" % impath)
        mod = SourceFileLoader(mod_name, impath).load_module()
        return mod

sys.modules[__name__] = _module()
