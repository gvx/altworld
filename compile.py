#import BaseHTTPServer
#import SimpleHTTPServer
import re
import os.path
#import posixpath
#import urllib

__version__ = "0.0"

f = open('template.txt')
TemplateText = f.read()
f.close()

def InsertPage(matchobj):
    page = os.path.join('src', matchobj.group(1))
    #if page:
    #    ctype, page = page
    try:
        f = open(page, 'r')
        txt = f.read()
        f.close()
      ##  print Wikify(txt)
        return Wikify(txt)
    except IOError as e:
        return 'ERROR: ' + str(e)

WikiSub = ((re.compile(r'\*(.*?)\*'), r'<strong>\1</strong>'),
           (re.compile(r'[[][[](.*?)[|](.*?)[]][]]'), r'<a href="\1.html">\2</a>'),
           (re.compile(r'[[][[](.*?)[]][]]'), r'<a href="\1.html">\1</a>'),
           ##(re.compile(r'[[]IMG[[](.*?)[]][]]'), r'<img src="\1">'),
           (re.compile(r"''(.*?)''"), r'<em>\1</em>'),
           (re.compile(r'^:(.*?)$', re.M), r'<h2>\1</h2>'),
           (re.compile(r'\n{2,}'), r'</p>\n\n<p>'),
##           (re.compile(r'(\r\n){2,}'), r'</p>\r\n\r\n<p>'),
           (re.compile(r'^'), r'<p>'),
           (re.compile(r'$'), r'</p>'),
           (re.compile(r'<p><h2>'), r'<h2>'),
           (re.compile(r'</h2></p>'), r'</h2>'),
           (re.compile(r'<p>{{(.*?)}}</p>'), InsertPage),
          )

def Wikify(text):
    for Regex, To in WikiSub:
        text = Regex.sub(To, text)
        ##print text
    return text

def Make(filename, source, outputfile):
    WikiText = source.read()
    WikiText = Wikify(WikiText)
    htmlText = TemplateText % {'text': WikiText, 'title': filename + ' - AltWorld'}
    outputfile.write(htmlText)

def CompileFile(arg, dir, files):
    for file in files:
        #continue
        try:
            print 'compiling', os.path.join('src', file), 'to', os.path.join('out', file)+'.html'
            fin = open(os.path.join('src', file))
            fout = open(os.path.join('out', file+'.html'), 'w')
            Make(file, fin, fout)
        except:
            print 'error in compiling', os.path.join('src', file)
        finally:
            fin.close()
            fout.close()

os.path.walk('src', CompileFile, None)
