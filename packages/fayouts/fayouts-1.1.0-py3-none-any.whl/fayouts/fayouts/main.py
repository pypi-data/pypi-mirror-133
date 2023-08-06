class FayoutError(Exception):
    pass

class Fayout:
    fayout = None
    def __init__(self, fayoutName):
        self.fayout = fayoutName

    def Read(self, field):
        file = open(f'{self.fayout}.fy', 'r', encoding='utf-8')
        lines = file.readlines()
        for line in lines:
            lineForTest = line.split(' = ')
            if(lineForTest[0] == field):
                return(lineForTest[1])

    def New(self, field, meaning):
        file = open(f'{self.fayout}.fy', 'r', encoding='utf-8')
        lines = file.readlines()
        for line in lines:
            lineForTest = line.split(' = ')
            if(lineForTest[0] == field):
                raise FayoutError('A field with the same name already exists.')
        file.close()
        file = open(f'{self.fayout}.fy', 'a', encoding='utf-8')
        file.write(f'\n{field} = {meaning}')

    def Edit(self, field, meaning):
        file = open(f'{self.fayout}.fy', 'r', encoding='utf-8')
        lines = file.readlines()
        i = ''
        for line in lines:
            lineForTest = line.split(' = ')
            if(lineForTest[0] == field):
                i = lines.index(line)
        if i == '': raise FayoutError('Field not found')
        file.close()
        lines[i] = f'{field} = {meaning}'

        inf = ''

        for line in lines:
            inf = inf + line

        file = open(f'{self.fayout}.fy', 'w', encoding='utf-8')
        file.write(inf)

    def GetIndex(self, field):
        file = open(f'{self.fayout}.fy', 'r', encoding='utf-8')
        lines = file.readlines()
        i = ''
        for line in lines:
            lineForTest = line.split(' = ')
            if(lineForTest[0] == field):
                i = lines.index(line)
        if i == '': raise FayoutError('Field not found')
        return i
    
    def Delete(self, field):
        file = open(f'{self.fayout}.fy', 'r', encoding='utf-8')
        lines = file.readlines()
        i = ''
        for line in lines:
            lineForTest = line.split(' = ')
            if(lineForTest[0] == field):
                i = lines.index(line)
        if i == '': raise FayoutError('Field not found')
        file.close()
        lines[i] = f''

        inf = ''

        for line in lines:
            inf = inf + line

        file = open(f'{self.fayout}.fy', 'w', encoding='utf-8')
        file.write(inf)

    def FPop(self):
        file = open(f'{self.fayout}.fy', 'r', encoding='utf-8')
        lines = file.readlines()
        file.close()
        
        inf = ''
        lines[0] = ''

        for line in lines:
            inf = inf + line

        file = open(f'{self.fayout}.fy', 'w', encoding='utf-8')
        file.write(inf)

    def LPop(self):
        file = open(f'{self.fayout}.fy', 'r', encoding='utf-8')
        lines = file.readlines()
        file.close()
        
        inf = ''
        lines[-1] = ''

        for line in lines:
            inf = inf + line

        file = open(f'{self.fayout}.fy', 'w', encoding='utf-8')
        file.write(inf)