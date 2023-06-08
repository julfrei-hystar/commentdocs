import os
import re
from pygments import highlight
from pygments.filter import simplefilter
from pygments.token import Comment
from pygments.lexers import get_lexer_by_name
from pygments.formatters import NullFormatter

# custom filter to only extract comments
@simplefilter
def commentsonly(self, lexer, stream, options):
    for ttype, value in stream:
        if ttype in Comment:
            yield ttype, value

# custom filter to remove comment delimiters
@simplefilter
def removedelimiters(self, lexer, stream, options):
    for ttype, value in stream:
        value = value.replace("/*", "")
        value = value.replace("*/", "\n")
        value = value.replace("//", "")
        value = value.strip(' ')
        value += '\n'
        yield ttype, value

# choose lexer and add filters
lexer = get_lexer_by_name("modelica", stripall=True)
lexer.add_filter(commentsonly())
lexer.add_filter(removedelimiters())

# choose formatter
formatter = NullFormatter()

# iterate through modelica files in current directory
for subdir, dirs, files in os.walk('.'):
    for file in files:
        filepath = os.path.join(subdir, file)
        if filepath.endswith(".mo"):
            # read code from file
            source = open(filepath, 'r')
            code = source.read()
            source.close()
            
            # apply lexer (including filters) and formatter to code
            result = highlight(code, lexer, formatter)
            
            # write result to file
            output = open(re.sub('.mo$', '.md', filepath), 'w')
            output.write(result)
            output.close()
