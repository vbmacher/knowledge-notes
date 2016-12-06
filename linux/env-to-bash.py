#!/usr/bin/python

import sys,re

# tokens must be as disjoint as possible! otherwise tokenizer might produce wrong tokens.
# if not possible, ordered correctly in TOKENS array
COMMENT   = r"(;|\#)[^\n]*"
STRING    = r"(\"[^\"\#;]*\")|(\'[^\'\#;]*\')"
ID        = r"[^\s\"\'\=\\\#;]+"
EQ        = r"\="
WORD      = r"[^\s\"\'\\\#;]+"
BACKSLASH = r"\\[ \t\r\f\v]*\n"
EOL       = r"\n"
SPACE     = r"[ \t\r\f\v]+"
UNKNOWN   = r".*"

# don't play with the order!
TOKENS = [COMMENT,STRING,BACKSLASH,ID,EQ,WORD,EOL,SPACE,UNKNOWN]
TOKENS_STRINGS={
  COMMENT: "COMMENT",STRING:"STRING",BACKSLASH:"BACKSLASH",ID:"ID",EQ:"EQ",WORD:"WORD",EOL:"EOL",SPACE:"SPACE",UNKNOWN:"UNKNOWN"
}


def tokenize(text):
  result = []
 
  while text:
    try:
      regex, match = matches = [
        (r, re.match(r, text, re.M))
        for r in TOKENS if re.match(r, text, re.M) is not None
      ][0]

      result += [(regex, text[match.start():match.end()])]
      text = text[match.end():]
    except:
      print "Input not recognized: ", text
      sys.exit(1)
  return result

def print_tokens(tokens):
  for t in tokens:
    print TOKENS_STRINGS[t[0]], t[1]


# recursive-descent parser

class Bashenizer:
  def __init__(self, tokens):
    self._tokens = tokens
    self._pos = 0

  def _token(self):
    self._pos += 1
    if self._pos - 1 >= len(tokens):
      return None
    return tokens[self._pos - 1]
  
  def _back(self):
    self._pos -= 1

  def _parse(self, d, allow_empty=True):
    t = self._token();
    if allow_empty and not t:
      return
    parsed = d[t[0]] if t[0] in d else self._error(t[1])
    if type(parsed) is dict:
      self._parse(parsed, allow_empty)
    else:
      for p in parsed:
        p(t)

  def _error(self,text):
    raise ValueError("Syntax error: " + text)

  # helper:
  def _print(self,t):
    sys.stdout.write(t[1])

  def _bs(self):
    print " \\"


  # grammar

  def start(self,t=None):
    self._parse({
      COMMENT: [self._start_repeat],
      ID: [ self._print, self._parse({
        EQ: [self._print, self._svalue, self._start_repeat]
      })]
    })

  def _start_repeat(self,t=None):
    self._parse({
      EOL: [self.start],
      UNKNOWN: [ self._back ]
    })

  def _svalue(self,t=None):
    self._parse({
      SPACE: [ self._svalue ],
      WORD: [self._print, self._svalue ],
      ID: [ self._print, self._svalue ],
      BACKSLASH: [ self._bs, self._svalue ],
      UNKNOWN: [ self._back ]
    })
    

rawinput = sys.stdin.read()
tokens = tokenize(rawinput)

#print "Tokens:"
#print_tokens(tokens)
print
print

bashenizer = Bashenizer(tokens)
bashenizer.start()

print
