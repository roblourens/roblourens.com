import re, sys

def fixURL(line):
    urlMatch = re.search('"(.*)"', line)
    if urlMatch:
        url = urlMatch.group(1)
        displayUrl = url.replace('http://', '').replace('https://', '').replace('www.', '')
        if '@' in url:
            url = 'mailto:'+url

        return line[:urlMatch.start()] + '<a href="' + url + '">' + displayUrl + '</a>' + line[urlMatch.end():]
    else:
        return line

def fixSpecialHTML(line):
    specialMatch = re.search('{{(.*)}}', line) 
    if specialMatch:
        specialName = specialMatch.group(1)
        return line[:specialMatch.start()] + '<span class="special" id="' + specialName + '">' + specialName + '</span>' + line[specialMatch.end():]
    else:
        return line

def addLineNumber(line, lineNum):
    if lineNum < 10:
        lineNum = '&nbsp;'+str(lineNum)
    return '<tr><td class="gutterText">'+str(lineNum)+'</td><td class="code"><pre>'+line+'</pre></td></tr>'

def fixLine(line, lineNum):
    line = fixURL(line)
    line = fixSpecialHTML(line)
    line = addLineNumber(line, lineNum)
    return line

def rlcomFormat(inPath, outPath):
    inFile = open(inPath, 'r')
    outFile = open(outPath, 'w')

    lineNum = 1
    for line in inFile:
        outFile.write(fixLine(line, lineNum))
        lineNum += 1
    
    inFile.close()
    outFile.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: format.py <inpath> <outpath>')
    else:
        rlcomFormat(sys.argv[1], sys.argv[2])
