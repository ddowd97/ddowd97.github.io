#!/usr/bin/python
# Python Interpreter is 3.8.2, ran through PyCharm 2019.3.3

# Name:             David Dowd
# ECN Login:        ddowd

from operator import itemgetter
import sys
import time
import cgi, cgitb

form = cgi.FieldStorage()

wordDictionary = {}

#with open('ScrabbleDictionary.txt', "r") as scrabbleDictionary:

with open('chosenDict.txt', "r") as chosenDict:
    chosenDictName = chosenDict.readline()

with open(chosenDictName, "r") as scrabbleDictionary:
    for line in scrabbleDictionary:
        line = line.replace('\t', ' ')
        wordDictionary[line.split(' ', 1)[0]] = line.split(' ', 1)[1]


letterList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
letterPointDict = { "a": 1, "b": 3, "c": 3, "d": 2, "e": 1, "f": 4, "g": 2, "h": 4, "i": 1, "j": 8, "k": 5, "l": 1, "m": 3,
                    "n": 1, "o": 1, "p": 3, "q": 10, "r": 1, "s": 1, "t": 1, "u": 1, "v": 4, "w": 4, "x": 8, "y": 4, "z": 10
}

# Modified implementation of the Steinhaus-Johnson-Trotter algorithm by rosettacode.org
# Original source: https://rosettacode.org/wiki/Permutations_by_swapping#Python
def permutation(n):
    sign = 1
    p = [[i, 0 if i == 0 else -1]
         for i in range(n)]

    yield tuple(pp[0] for pp in p), sign

    while any(pp[1] for pp in p):
        i1, (n1, d1) = max(((i, pp) for i, pp in enumerate(p) if pp[1]), key=itemgetter(1))
        sign *= -1
        if d1 == -1:
            i2 = i1 - 1
            p[i1], p[i2] = p[i2], p[i1]
            if i2 == 0 or p[i2 - 1][0] > n1:
                p[i2][1] = 0
        elif d1 == 1:
            i2 = i1 + 1
            p[i1], p[i2] = p[i2], p[i1]
            if i2 == n - 1 or p[i2 + 1][0] > n1:
                p[i2][1] = 0
        yield tuple(pp[0] for pp in p), sign

        for i3, pp in enumerate(p):
            n3, d3 = pp
            if n3 > n1:
                pp[1] = 1 if i3 < i2 else -1
              
cont = 0
flag = 1
bestPoints = 0
temp = str(form.getvalue('temp'))
if len(temp) == 7:
    cont = 1
    flag = 0
#boardTimeStart = time.time()
#if checkBoard(sampleBoardArray1, sampleBoardArray1Mod) == True:
#    print("Board is valid!")
#else:
#    print("Board is invalid, try again!")
#print("Board check took {} seconds.".format(time.time() - boardTimeStart))
while cont == 1:
    start = time.time()
    permList = []
    totalPermList = []
    new_temp = ''
    flag = 0
    defFlag = ''
    size_counter = 7
    tempPoints = 0
    bestPoints = 0
    bestWord = ''

    for i in permutation(size_counter):
        x = 0
        while x < len(i[0]):
            new_temp = new_temp + temp[i[0][x]]
            x += 1
        permList.append(new_temp)
        new_temp = ''
    
    
    for new_temp in permList:
        if '*' in new_temp: # Wildcard Blank. Unsure if that tile will be used in our design though.
            z = 0
            while z < 26:
                replace_temp = new_temp.replace('*', letterList[z])
                if replace_temp.upper() in wordDictionary and replace_temp not in totalPermList:
                    totalPermList.append(replace_temp)
                    y = 0
                    tempPoints = 0
                    while y < size_counter:
                        tempPoints = tempPoints + letterPointDict[replace_temp[y]]
                        y += 1
                    if tempPoints > bestPoints:
                        bestPoints = tempPoints + 50
                        bestWord = replace_temp
                z += 1
        elif new_temp.upper() in wordDictionary and new_temp not in totalPermList:
            y = 0
            tempPoints = 0
            while y < size_counter:
                tempPoints = tempPoints + letterPointDict[new_temp[y]]
                y += 1
            if tempPoints > bestPoints:
                bestPoints = tempPoints + 50
                bestWord = new_temp
    size_counter -= 1
    while size_counter > 1:
        for perm in permList:
            new_temp = perm[0:size_counter]
            if '*' in new_temp:  # Wildcard Blank. Unsure if that tile will be used in our design though.
                z = 0
                while z < 26:
                    replace_temp = new_temp.replace('*', letterList[z])
                    if replace_temp.upper() in wordDictionary and replace_temp not in totalPermList:
                        totalPermList.append(replace_temp)
                        y = 0
                        tempPoints = 0
                        while y < size_counter:
                            tempPoints = tempPoints + letterPointDict[replace_temp[y]]
                            y += 1
                        if tempPoints > bestPoints:
                            bestPoints = tempPoints
                            bestWord = replace_temp
                    z += 1
            elif new_temp.upper() in wordDictionary and new_temp not in totalPermList:
                totalPermList.append(new_temp)
                y = 0
                tempPoints = 0
                while y < size_counter:
                    tempPoints = tempPoints + letterPointDict[new_temp[y]]
                    y += 1
                if tempPoints > bestPoints:
                    bestPoints = tempPoints
                    bestWord = new_temp
        size_counter -= 1
    cont = 0
                
#form = cgi.FieldStorage()
#temp = form.getvalue('temp')
print("Content-type:text/html\r\n\r\n")
print('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">')
print('<html>')
print('<html xmlns="http://www.w3.org/1999/xhtml">')
print('<head>')

print('<style>')
print('.center {')
print(' display: block;')
print(' margin-left: auto;')
print(' margin-right: auto;')
print('}')
# CSS Sample from Source: https://www.w3schools.com/howto/howto_js_accordion.asp
print('.accordion {')
print('  background-color: #eee;')
print('  color: #444;')
print('  cursor: pointer;')
print('  padding: 18px;')
print('  width: 100%;')
print('  text-align: left;')
print('  border: none;')
print('  outline: none;')
print('  transition: 0.4s;')
print('}')
# CSS Sample from Source: https://www.w3schools.com/howto/howto_js_accordion.asp
print('.active, .accordion:hover {')
print('  background-color: #ccc;')
print('}')
# CSS Sample from Source: https://www.w3schools.com/howto/howto_js_accordion.asp
print('.panel {')
print('  padding: 0 18px;')
print('  background-color: white;')
print('  display: none;')
print('  overflow: hidden;')
print('}')
# CSS Sample from Source: https://www.w3schools.com/html/html_tables.asp
print('table {')
print('  font-family: arial, sans-serif;')
print('  border-collapse: collapse;')
print('  width: 100%;')
print('}')
# CSS Sample from Source: https://www.w3schools.com/html/html_tables.asp
print('td, th {')
print('  border: 1px solid #cccccc;')
print('  text-align: left;')
print('  padding: 8px;')
print('}')
# CSS Sample from Source: https://www.w3schools.com/html/html_tables.asp
print('tr:nth-child(even) {')
print('  background-color: #eeeeee;')
print('}')
print('</style>')

print('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
print('<base href="https://engineering.purdue.edu/477grp15/" />')
print('<title>Word Recommended!</title>')
print('<meta name="keywords" content="" />')
print('<meta name="description" content="" />')
print('<meta name="author" content="George Hadley">')
print('<meta name = "format-detection" content = "telephone=no" />')
print('<meta name="viewport" content="width=device-width,initial-scale=1.0">')
print('<link rel="stylesheet" href="css/default.css" type="text/css" media="all" />')
print('<link rel="stylesheet" href="css/responsive.css">')
print('<link rel="stylesheet" href="css/styles_new.css">')
print('<link rel="stylesheet" href="css/content.css">')
print('</head>')



print('<body>')
print('<div id="wrapper_site">')
print('    <div id="wrapper_page">')
print('    <div id="header"></div>')
print('    <div id="menu"></div>')
print('    <div id="banner">')
print('        <img src="Team/img/BannerImgExample.jpg"></img>')
print('    </div>')
print('    <div id="content">')
print('        <button class="accordion">Rules of Dabble</button>')
print('        <div class="panel">')
print('          <p>1) Players take turns placing one word at a time on the Dabble board.<br>')
print('             2) Players may pass their turn, if they so choose.<br>')
print('             3) Words placed on the board must be defined in the current dictionary.<br>')
print('             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a) Placed words must not, as a consequence, form other words that are not defined in the current dictionary.<br>')
print('             4) The first word placed must use the center of the board.<br>')
print('             5) Words placed on the board must be connected to all other previously placed words.<br>')
print('             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a) Placed words must either EXTEND, HOOK, or be PARALLEL to previous words.<br>')
print('             6)The game ends when the score limit [if specified] is reached or when six consecutive passes occur.')
print('          </p>')
print('    </div>')
print('        <button class="accordion">Scoring System</button>')
print('        <div class="panel">')
print('          <p>1) A bonus space (<b>DL</b>, <b>TL</b>, <b>DW</b>, <b>TW</b>) is only used one time - when a new letter is placed on it.<br>')
print('             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a) <b>DL</b> = Double Letter, <b>TL</b> = Triple Letter, <b>DW</b> = Double Word, <b>TW</b> = Triple Word<br>')
print('             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i) The center of the board is a <b>DW</b> bonus space.<br>')
print('             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b) Letter bonuses are applied before word bonuses - word bonuses come last!<br>')
print('             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;c) Word bonuses are applied to all words directly formed by that placed tile.<br>')
print('             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i) Word bonuses are stackable - 2 <b>DW</b> ("Double-Double") is a x4 bonus, 2 <b>TW</b> ("Triple-Triple") is a x9 bonus!<br>')
print('             2) Using all 7 tiles in one turn is a BINGO and awards 50 extra points (after bonus space calculation)!<br>')
print('             3) No points are deducted when passing a turn.')
print('          </p>')
print('    </div>')
print('        <button class="accordion">Letter Point Distribution</button>')
print('        <div class="panel">')
print('          <p><table>')
print('              <tr><th>Letter</th><th>Points</th></tr>')
print('              <tr><td>A</td><td>1</td></tr>')
print('              <tr><td>B</td><td>3</td></tr>')
print('              <tr><td>C</td><td>3</td></tr>')
print('              <tr><td>D</td><td>2</td></tr>')
print('              <tr><td>E</td><td>1</td></tr>')
print('              <tr><td>F</td><td>4</td></tr>')
print('              <tr><td>G</td><td>2</td></tr>')
print('              <tr><td>H</td><td>4</td></tr>')
print('              <tr><td>I</td><td>1</td></tr>')
print('              <tr><td>J</td><td>8</td></tr>')
print('              <tr><td>K</td><td>5</td></tr>')
print('              <tr><td>L</td><td>1</td></tr>')
print('              <tr><td>M</td><td>3</td></tr>')
print('              <tr><td>N</td><td>1</td></tr>')
print('              <tr><td>O</td><td>1</td></tr>')
print('              <tr><td>P</td><td>3</td></tr>')
print('              <tr><td>Q</td><td>10</td></tr>')
print('              <tr><td>R</td><td>1</td></tr>')
print('              <tr><td>S</td><td>1</td></tr>')
print('              <tr><td>T</td><td>1</td></tr>')
print('              <tr><td>U</td><td>1</td></tr>')
print('              <tr><td>V</td><td>4</td></tr>')
print('              <tr><td>W</td><td>4</td></tr>')
print('              <tr><td>X</td><td>8</td></tr>')
print('              <tr><td>Y</td><td>4</td></tr>')
print('              <tr><td>Z</td><td>10</td></tr>')
print('             </table>')
print('          </p>')
print('        </div>')
# The following <script> is borrowed from the source https://www.w3schools.com/howto/howto_js_accordion.asp
print('        <script>')
print('        var acc = document.getElementsByClassName("accordion");')
print('        var i;')

print('        for (i = 0; i < acc.length; i++) {')
print('          acc[i].addEventListener("click", function() {')
print('            this.classList.toggle("active");')
print('            var panel = this.nextElementSibling;')
print('            if (panel.style.display === "block") {')
print('              panel.style.display = "none";')
print('            } else {')
print('              panel.style.display = "block";')
print('            }')
print('          });')
print('        }')
print('        </script>')
print('        <br><br>')
print('        <FORM action="var/www/cgi-bin/loadDabble.py" method="get">')
print('            <INPUT TYPE="Submit" Value="REFRESH">')
print('        </FORM>')
print('        <h2>Dabble Dictionary Support</h2>')
print('        <FORM action="var/www/cgi-bin/chooseDict.py" method="get">')
if chosenDictName == 'CollinsDictionary.txt':
  print('            Collins Dictionary<input type="radio" name="dict" value="1" checked> Chosen!<br>')
  print('            Oxford English Dictionary<input type="radio" name="dict" value="2"><br>')
  print('            Word Dump <i>(<b>Experimental</b> - Some Undefined/Obscure Words, Longer Processing Time)</i><input type="radio" name="dict" value="3"><br>')
elif chosenDictName == 'OxfordEnglishDictionary.txt':
  print('            Collins Dictionary<input type="radio" name="dict" value="1"><br>')
  print('            Oxford English Dictionary<input type="radio" name="dict" value="2" checked> Chosen!<br>')
  print('            Word Dump <i>(<b>Experimental</b> - Some Undefined/Obscure Words, Longer Processing Time)</i><input type="radio" name="dict" value="3"><br>')
else:
  print('            Collins Dictionary<input type="radio" name="dict" value="1"><br>')
  print('            Oxford English Dictionary<input type="radio" name="dict" value="2"><br>')
  print('            Word Dump <i>(<b>Experimental</b> - Some Undefined/Obscure Words, Longer Processing Time)</i><input type="radio" name="dict" value="3" checked> Chosen!<br>')
print('            <INPUT TYPE="Submit" Value="Choose my dictionary!">')
print('        </FORM>')
print('        <br>')
print('        <h2>Dabble Word Checker</h2>')
print('        <FORM action="var/www/cgi-bin/wordCheck.py" method="get">')
print('            Please enter your word (e.g. "pencil"):<br>')
print('            <INPUT TYPE="Text" Size="3" maxlength="7" name="temp">&nbsp;<INPUT TYPE="Submit" Value="Check my word!">')
print('        </FORM>')
print('        <br>')
print('        <h2>Dabble Word Recommender</h2>')
print('        <FORM action="var/www/cgi-bin/permuteCheck.py" method="get">')
if chosenDictName == 'CollinsDictionary.txt':
    print("            Please enter your 7 letters (e.g. 'abcdefg'). Keep in mind that the current dictionary in play is Collin's Dictionary.<br>")
elif chosenDictName == 'OxfordEnglishDictionary.txt':
    print("            Please enter your 7 letters (e.g. 'abcdefg'). Keep in mind that the current dictionary in play is the Oxford English Dictionary.<br>")
else:
    print("            Please enter your 7 letters (e.g. 'abcdefg'). Keep in mind that the current dictionary in play is the Word Dump.<br>")
print('            <INPUT TYPE="Text" Size="3" maxlength="7" name="temp">&nbsp;<INPUT TYPE="Submit" Value="Recommend me a word!">')
print('            <br><br>')
if bestPoints > 0:
    if len(bestWord) >= 7:
        print('Bingo! 50 Bonus Points!<br>')
    if bestPoints > 100:
        print('The best word found was <b>%s</b>, which is worth <b>%d</b> points!!!<br>' % (bestWord.upper(), bestPoints))
    elif bestPoints > 50:
        print('The best word found was <b>%s</b>, which is worth <b>%d</b> points!!<br>' % (bestWord.upper(), bestPoints))
    elif bestPoints > 25:
        print('The best word found was <b>%s</b>, which is worth <b>%d</b> points!<br>' % (bestWord.upper(), bestPoints))
    else:
        print('The best word found was <b>%s</b>, which is worth <b>%d</b> points.<br>' % (bestWord.upper(), bestPoints))
    print('Definition: <i>%s</i><br>' % wordDictionary[bestWord.upper()])
elif flag == 1:
    print('<b>Please enter 7 letters (no less).</b>')
else:
    print('No possible words could be found..')
print('        </FORM>')
print('        <br>')
print('        <h2>Dabble Board Verifier</h2>')
print('        <FORM action="var/www/cgi-bin/boardCheck.py" method="get">')
'''
print('            <img src="Team/progress/img/board1.png" width=281 height=142>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
print('            <img src="Team/progress/img/board2.png" width=281 height=142>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
print('            <img src="Team/progress/img/board3.png" width=281 height=142><br>')
if boardVal == 1:
    print('            &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Board1<input type="radio" name="board" value="1" checked>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;')
else:
    print('            &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Board1<input type="radio" name="board" value="1">&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;')
if boardVal == 2:
    print('            &emsp;&emsp;Board2<input type="radio" name="board" value="2" checked>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;')
else:
    print('            &emsp;&emsp;Board2<input type="radio" name="board" value="2">&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;')
if boardVal == 3:
    print('            Board3<input type="radio" name="board" value="3" checked><br><br>')
else:
    print('            Board3<input type="radio" name="board" value="3"><br><br>')
'''
print('            <img src="var/www/cgi-bin/boardImage.png" width=280 height=280 class="center"><br>')
print('            <p style="text-align:center">Current Board<input type="radio" name="board" value="1" checked></p><br>')
print('            <p style="text-align:center">(Enter <b>CTRL + F5</b> if the image does not refresh on your screen.)')
print('            <p style="text-align:center"><INPUT TYPE="Submit" Value="Check my board!">')
print('        </FORM>')
print('    </div>')
print('    <div id="footer"></div>')
print('    </div>')
print('</div>')

print('<script src="js/jquery.js"></script>')
print('<script src="js/jquery-migrate-1.1.1.js"></script>')
print('<script type="text/javascript">')
print('$(document).ready(function() {')
print('    $("#header").load("header.html");')
print('    $("#menu").load("navbar_new.html");')
print('    $("#member1").load("Team/czatloko.html");')
print('    $("#member2").load("Team/delagarm.html");')
print('    $("#member3").load("Team/wilso822.html");')
print('    $("#member4").load("Team/ddowd.html");')
print('    $("#footer").load("footer.html");')
print('});')
print('</script>')
print('</body>')
print('</html>')