import pydoc
import os
import constitch
import starcall
import re
import inspect

class CustomHTMLDoc(pydoc.HTMLDoc):
    def markup(self, text, escape=None, funcs={}, classes={}, methods={}):
        """Mark up some plain text, given a context of symbols to look for.
        Each context dictionary maps object names to anchor names."""
        escape = escape or self.escape
        results = []
        here = 0
        pattern = re.compile(r'\b((http|https|ftp)://\S+[\w/]|'
                                r'RFC[- ]?(\d+)|'
                                r'PEP[- ]?(\d+)|'
                                r'(self\.)?([.\w]*\w))')
        while True:
            match = pattern.search(text, here)
            if not match: break
            start, end = match.span()
            results.append(escape(text[here:start]))

            all, scheme, rfc, pep, selfdot, name = match.groups()
            if scheme:
                url = escape(all).replace('"', '&quot;')
                results.append('<a href="%s">%s</a>' % (url, url))
            elif rfc:
                url = 'http://www.rfc-editor.org/rfc/rfc%d.txt' % int(rfc)
                results.append('<a href="%s">%s</a>' % (url, escape(all)))
            elif pep:
                url = 'https://www.python.org/dev/peps/pep-%04d/' % int(pep)
                results.append('<a href="%s">%s</a>' % (url, escape(all)))
            else:
                if name in methods or name in funcs or name in classes:
                    results.append(selfdot if selfdot else '' + self.namelink(name, methods, funcs, classes))
                else:
                    #results.append(name)
                    obj = None
                    try:
                        if name.count('.'):
                            obj = eval(current_module.__name__ + '.' + name)
                        #print (obj, name, current_module.__name__ + '.' + name)
                    except:
                        pass

                    if not obj:
                        try:
                            obj = eval(name)
                            #print (obj, name)
                        except:
                            pass

                    link = None
                    if obj:
                        if obj == fisseq.stitching.Aligner.align:
                            print (obj, inspect.isfunction(obj), inspect.ismethod(obj))
                            print (obj.__module__)
                            print (obj.__self__)
                            print (obj.__module__)
                        if inspect.isfunction(obj):
                            #if hasattr(obj, '__module__'):
                                link = obj.__module__ + '.html#-' + obj.__name__
                        elif inspect.ismethod(obj):
                            #if hasattr(obj, '__self__'):
                                link = obj.__self__.__module__ + '.html#' + obj.__self__.__name__ + '-' + obj.__name__
                        elif type(obj) == type:
                            link = obj.__module__ + '.html#' + obj.__name__
                        elif type(obj) == type(fisseq):
                            link = obj.__name__ + '.html'

                    if name == 'CompositeImage.load':
                        print (name, obj, link)
                        
                    if link:
                        results.append('<a href="{}">{}</a>'.format(link, name))
                    else:
                        results.append(name)
            """
            elif selfdot:
                # Create a link for methods like 'self.method(...)'
                # and use <strong> for attributes like 'self.attr'
                if text[end:end+1] == '(':
                    results.append('self.' + self.namelink(name, methods))
                else:
                    results.append('self.<strong>%s</strong>' % name)
            elif text[end:end+1] == '(':
                results.append(self.namelink(name, methods, funcs, classes))
            else:
                results.append(self.namelink(name, classes))
            """
            here = end
        results.append(escape(text[here:]))
        return ''.join(results)

orig_getdoc = pydoc.getdoc
current_module = None

def getdoc(obj):
    global current_module
    if type(obj) == type(constitch):
        #print ('yoooo', obj)
        current_module = obj
    return orig_getdoc(obj)

pydoc.getdoc = getdoc

pydoc.HTMLDoc = CustomHTMLDoc

#pydoc.browse(40297, hostname='127.0.0.1', open_browser=False)
#pydoc.cli()

packages = [
    'constitch',
    'constitch.alignment',
    'constitch.composite',
    'constitch.constraints',
    'constitch.evaluation',
    'constitch.merging',
    'constitch.solving',
    'constitch.stage_model',
    'constitch.stitching',
    'constitch.utils',
    'starcall',
    'starcall.alignment',
    'starcall.correction',
    'starcall.dotdetection',
    'starcall.io',
    #'starcall.qc',
    'starcall.segmentation',
    'starcall.sequencing',
    'starcall.reads',
    #'starcall.stitching',
    'starcall.utils',
]

os.chdir('docs')
for package in packages:
    pydoc.writedoc(package)

