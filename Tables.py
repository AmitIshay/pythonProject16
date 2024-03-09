import csv, re
import json


row_count = 0
def removeZeros(str):
    words = str.split()
    filteredWord = [word for word in words if '0' in word and all(char == '0' for char in word)]
    outputWords = [word for word in words if word not in filteredWord]
    str = ' '.join(outputWords)
    return str.lstrip('0')
def replaceShortcut(str):
    replacePatterns = {
        r'\b(qu|qd|Q|Qu|QD|QU)\b': 'Quadra ',
        r'\b(trav|trv|TV)\b': 'Travessa ',
        r'\b(ap|apt|AP|Ap)\b': 'Apartamento ',
        r'\b(lt|lot|LT|Lt|LOTE|LO)\b': 'Loteamento ',
        r'\b(ave|av|AV|Av)\b': 'Avenida ',
        r'\b(BL|Bl|bl|block|BLOCK)\b': 'Bloco ',
        r'\b(CA|CS)\b': 'Casa ',
        r'(n\?|N\?|n\?:|N\?:)': 'Number '

    }
    str = re.sub(r'(\d)([a-zA-Z])|([a-zA-Z])(\d)', r'\1\3 \2\4', str)
    for pattern, replacement in replacePatterns.items():
        str = re.sub(pattern,replacement,str)
    return re.sub(r'\s+', ' ', str)

def replaceMarkInStreet(name):
    if name.startswith('.'):
        name = name[1:]
    if name.endswith('.'):
        name = name[:-1]
    characters = ['!','%','*',',','-','/',':',';','#','.']
    # re.sub(r'&#259;', 'a', name)
    # re.sub(r'&#1091;','y', name)
    # re.sub(r'&#1047;', 'c', name)
    # re.sub(r'&#30136;', 'ee', name)
    for char in characters:
        name = name.replace(char, '')
    if '?' in name:
        name = name.replace('?','a')
    if name.startswith('? ') or name.endswith(' ?'):
        name = name.replace('?', '')
    # if '!' in name:
    #     name = name.replace('!','')
    # if '%' in name:
    #     name = name.replace('%','')
    # if '*' in name:
    #     name = name.replace('*','')

    return name

def toUpperCase(str):
    return re.sub(r'[a-z]', lambda match: match.group().upper(), str)


def replaceToRJ(str):
    str = 'RJ'
    return str


def checkPhoneNum(num, prefix):
    if num == '0' or num.lstrip('0') == '':
        return ''
    removeLetters = re.sub(r'[a-zA-Z-]','',num)
    if len(removeLetters) > 9:
        return ''
    elif len(removeLetters) == 9:
        newNum = '+55' + prefix + removeLetters
        numFormat = f"{newNum[:3]} ({newNum[3:5]}) {newNum[5:10]}-{newNum[10:]}"
    elif len(removeLetters) == 8:
        newNum = '+55' + prefix + removeLetters
        numFormat = f"{newNum[:3]} ({newNum[3:5]}) {newNum[5:9]}-{newNum[9:]}"
    return numFormat

def insertStatePrefix(row):
    if row == '21':
        str = 'Greater Rio de Janeiro and Teresopolis'
    elif row == '22':
        str = 'East and North'
    elif row == '24':
        str = 'West'
    return str


def checkId(id):
    if id == '0' or id.lstrip('0') == '':
        return ''
    removeLetters = re.sub(r'[a-zA-Z]','',id)
    if len(removeLetters) > 11:
        removeZeros = removeLetters.lstrip('0')
        fixZeros = removeZeros[:11].zfill(11)
    else:
        fixZeros = removeLetters.zfill(11)
    if len(fixZeros) == 11:
        idFormat = f"{fixZeros[:3]}.{fixZeros[3:6]}.{fixZeros[6:9]}-{fixZeros[9:]}"
        return idFormat

    return fixZeros


def setCapitaleFirstLetter(name):
    words = name.split()
    capitalized_words = [word.capitalize() for word in words]
    return ' '.join(capitalized_words)

def replacePatterns(name):
    replacePatterns = {
        '&#259;' : 'a',
        '&#1091;' : 'y',
        '&#1047;' : 'c',
        '&#30136;' : 'ee',
        '&#227;' : 'a'
    }
    pattern = '|'.join(re.escape(key) for key in replacePatterns.keys())
    return re.sub(pattern, lambda match: replacePatterns[match.group()], name)

def replaceMarkInFullName(name):
    characters = ['!','%','*',',','-','/',':',';','#',"'"]
    # re.sub(r'&#259;', 'a', name)
    # re.sub(r'&#1091;','y', name)
    # re.sub(r'&#1047;', 'c', name)
    # re.sub(r'&#30136;', 'ee', name)
    for char in characters:
        name = name.replace(char, '')
    if '?' in name:
        name = name.replace('?','a')
    if name.startswith('? ') or name.endswith(' ?'):
        name = name.replace('?', '')
    # if '!' in name:
    #     name = name.replace('!','')
    # if '%' in name:
    #     name = name.replace('%','')
    # if '*' in name:
    #     name = name.replace('*','')
    if name.startswith('.'):
        name = name[1:]
    if name.endswith('.'):
        name = name[:-1]

    name = ''.join(char for char in name if not char.isdigit())

    while '(' in name and ')' in name:
        start_index = name.find('(')
        end_index = name.find(')')
        if start_index < end_index:
            name = name[:start_index] + name[end_index + 1:]
        else:
            break
    # if '(' in name:
    #     name = name.split('(', 1)[0]

    return name


with open("Untitled Workbook - Sheet3 (1).csv") as csv_file:
    reader = csv.reader(csv_file)
    headers = next(reader)
    for i, title in enumerate(headers):
        if not title:
            headers[i] = "city"
            headers[i+1] = "neighborhood"
            headers[i+2] = "street"
            headers[i+3] = "houseDetails1"
            headers[i+4] = "houseDetails2"

    for title in headers:
        print(title)

    csv_file.seek(0)  # Reset the file pointer to the beginning

    with open('new_table.csv','w') as new_file:
        csv_writer = csv.writer(new_file)
        csv_writer.writerow(headers)
        next(reader)
        for row in reader:
            row[0] = checkId(row[0])
            row[1] = replacePatterns(row[1])
            row[1] = replaceMarkInFullName(row[1])
            row[1] = setCapitaleFirstLetter(row[1])
            row[3] = insertStatePrefix(row[2])
            row[4] = checkPhoneNum(row[4], row[2])
            row[5] = replaceToRJ(row[5])
            row[6] = replacePatterns(row[6])
            row[6] = replaceMarkInFullName(row[6])
            row[6] = toUpperCase(row[6])
            row[7] = replacePatterns(row[7])
            row[7] = replaceMarkInFullName(row[7])
            row[7] = toUpperCase(row[7])
            row[8] = replacePatterns(row[8])
            row[8] = replaceShortcut(row[8])
            row[8] = replaceMarkInStreet(row[8])
            row[9] = replacePatterns(row[9])
            row[9] = replaceShortcut(row[9])
            row[9] = replaceMarkInStreet(row[9])
            row[9] = removeZeros(row[9])
            row[10] = replacePatterns(row[10])
            row[10] = replaceShortcut(row[10])
            row[10] = replaceMarkInStreet(row[10])
            row[10] = removeZeros(row[10])
            csv_writer.writerow(row)
            #row_count += 1
            #print(row[0])




print("Number of rows in the file:", row_count)
#data = pandas.read_csv("DE - Home Assignment.csv")
#print(data)
#data_dict = {
#    "students": ["a","b","c"],
#    "scores": [54,55,53],
#    "height": [4,5,4]
#}
#data = pandas.DataFrame(data_dict)
