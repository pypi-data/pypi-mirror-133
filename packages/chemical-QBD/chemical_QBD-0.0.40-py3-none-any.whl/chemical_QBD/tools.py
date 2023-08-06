from . import const

def read__sheet(sheet, output='list'):
    rows = sheet.split('\n')
    rows = [i for i in filter(None, rows)]
    for i in range(0,len(rows)):
        comment__position = rows[i].find('#')
        if comment__position == -1: continue
        else: rows[i] = rows[i][:comment__position]
    rows = [i for i in rows if ' ' in i]

    rows__elements = []
    rows__values = []

    for i in rows:
        line = i.split(' ')
        line = [i for i in filter(None, line)]
        if len(line) == 2:
            if is__consisted__of__chemical__elements(line[0]):
                rows__elements.append(line[0])
                rows__values.append(float(line[1]))

    if output == 'list':    return rows__elements, rows__values
    elif output == 'dict':  return dict(zip(rows__elements, rows__values))
    else:                   return rows__elements, rows__values




def is__consisted__of__chemical__elements(substance):
    if substance == '': return False

    for i in const.CHEMICAL__ELEMENTS__2:
        if i in substance:
            substance = substance.replace(i, '')

    for i in const.CHEMICAL__ELEMENTS__1:
        if i in substance:
            substance = substance.replace(i, '')

    if substance == '': return True
    else:               return False
    

def find__chemical__elements(compound):

    found__elements = []

    for element in const.CHEMICAL__ELEMENTS__2:
        if element in compound:
            found__elements.append(element)
            compound = compound.replace(element, '')

    for element in const.CHEMICAL__ELEMENTS__1:
        if element in compound:
            found__elements.append(element)
            compound = compound.replace(element, '')

    return found__elements

