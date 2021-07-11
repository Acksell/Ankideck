"""
Reads words from an input file with a more input-friendly format
and formats it to a semicolon separated "csv" so that Anki can import it.

The format of the file is such that the front of the card is the first
field and the back is the second field, separated by "-":

  <front text> - <back text>

Example: 
  
  Waldeinsamkeit - the feeling of being alone in the woods - bokstavligen skogsensamhet
"""

INPUT_FILE = "glossary.txt"
OUTPUT_FILE = "deck.txt"
SORT = True # alphabetically

def convert(line): # (line string, ok bool)
  if "-" not in line:
    return line, False
  word = getWord(line)
  answer = getAnswer(line)
  if not word:
    print("no word", answer)
  if not answer:
    print("no answer", word)
  return ";".join((wrap(word),answer)), True

def getWord(line):
  return wrap(line.split("-")[0].strip())

def getAnswer(line):
  return wrap("-".join(line.split("-")[1:]).strip())

# Wraps field with quotes because otherwise Anki doesn't recognize it correctly.
def wrap(string): 
  if string[0] == '"' and string[-1] == '"':
    return string
  else:
    return f"\"{string}\""


with open(OUTPUT_FILE, 'w+', encoding='utf-8') as deck:
  with open(INPUT_FILE, 'r',encoding='utf-8') as glossary:
    seen = dict()
    words = list()
    lines = list()
    while line := glossary.readline():  
      line, ok = convert(line)
      if ok:
        lines.append(line)
        if seen.get(word := getWord(line).lower()):
          print("duplicate", word)
        else:
          words.append(word.lower())
          seen[word.lower()]=line
      else:
        print("Bad input:", line)
    if SORT:
      words.sort()
      lines = list(seen[word] for word in words)
    deck.write("\n".join(lines))


