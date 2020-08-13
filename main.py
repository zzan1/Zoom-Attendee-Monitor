import os
import re
import shutil

import pandas as pd


def getIdAndName(filepath):
    with open(filepath, 'r', encoding='utf') as f:
        content = f.read().split('\n')

    regex = re.compile(r"^(?P<id>\d{1,3})[ \-_–－~—+]*(?P<name>[\u4e00-\u9fa5 ]{2,4}).*")

    id_array = []
    name_array = []

    for item in content:
        matches = regex.search(item)
        if matches:
            id_array.append(int(matches.group('id')))
            name_array.append(matches.group('name'))

    data = pd.DataFrame({'学号': id_array, filepath.split("\\")[1].split('.')[0] : name_array})
    return data.sort_values('学号')

def targetStudents():
    targetFile = r'target\3个群的学号分配-20200731.xlsx'

    studentGroup_one = pd.read_excel(targetFile, '1群学号分配')
    studentGroup_two = pd.read_excel(targetFile, '2群学号分配')
    studentGroup_three = pd.read_excel(targetFile, '3群学号分配')

    totalStudent = pd.concat([studentGroup_one, studentGroup_two, studentGroup_three], axis=0)
    return totalStudent

def integrate(totalStudent):
    signInDir = r'attendee'
    checkedDir = r'attendee\checked'

    fileName = os.listdir(signInDir)
    fileName.remove('checked')
    for index, item in enumerate(fileName):
        # get all the file in signInDir
        filepath = os.path.join(signInDir, item)
        result  = getIdAndName(filepath)
        result = result.drop_duplicates(subset=['学号'])
        try:
            if not result.empty and index == 0:
                intergration = pd.merge(totalStudent, result, how='left', on='学号')
            elif not result.empty:
                intergration = pd.merge(intergration, result, how='left', on='学号')
        except:
            print('%s is error' % filepath)
        finally:
            shutil.move(filepath, checkedDir)
    
    return intergration


if __name__ == '__main__':
    totalStudent = targetStudents()

    intergration = integrate(totalStudent)
    with pd.ExcelWriter('intergration.xlsx') as writer:
        intergration.to_excel(writer)
