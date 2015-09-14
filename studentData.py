import pandas as pd
import numpy as np
import json

valid_grades = ['K','1','2','3','4','5','6','7','8','9','10','11','12']

def convert_boolean(x,booleanDefault = False):
    '''
    Converts and Normalizes data for the district data.
    I am assuming the data is boolean and converting t to True and f to False
    And making all lowercase
    '''
    if type(x) != str:
        return  booleanDefault
    if x.lower() in ['f', 'false']:
        return False
    elif x.lower() in ['t', 'true']:
        #print(x)
        return True
    else:
        return booleanDefault

def cleanTestData(testData):
    '''
    Cleaning/Normalizing up subject or test data.
    '''
    return testData.str.strip().str.lower()

def cleanDistrictData(districtData):
    '''
    Cleaning/Normalizing/Comverting to boolean the district data
    '''
    return districtData.str.strip().str.lower().map(convert_boolean)

def mask(df,f):
    return df[f(df)]

pd.DataFrame.mask = mask

def processSchema(df):
    '''
    Generating Schema Object from the dataFrame
    '''
    # Mapping of types to schema fields
    map_dtypes_type = {
        "int64": "integer",
        "object": "string",
        "float64": "decimal",
        "bool": "boolean"
    }
    columns = []
    # columns.append( {"name": "student_id", "type":"integer" , "examples" : [1,2,3]})
    # columns.append( {"name":"test", "type":"string" , "examples" : ["math","reading","science"],"limit":7})
    for i, j in zip(df.columns, df.dtypes):
        k = df[i].unique()[:5].tolist()
        mapType = map_dtypes_type.get(str(j))
        if (mapType == 'string'):
            columns.append({"name": str(i), "type": mapType, "examples": k, "limit": int(df[i].str.len().max())})
        else:
            columns.append({"name": str(i), "type": mapType, "examples": k})
    obj1 = {"columns": columns}
    #print(json.dumps(obj1, indent=4))
    return obj1

def write_to_file(fileName='schmema.json',data=None):
    '''
    Based on the Schema Object generates json representation of Schema and writes
    into a file
    '''
    if data is None:
        return
    with open(fileName,'w') as outfile:
        json.dump(data,fp=outfile, indent=4)

def check_fields(df):
    '''
    Checks if all the fields are in data frame
    '''
    valid_fields = ['student_id','score','grade','test','district']
    missing_fields = None
    for i in valid_fields:
        if i not in df.columns:
            missing_fields = str(missing_fields) + i
    return missing_fields

def data_import(df=None):
    '''
    Loads the file and generates data frame
    and calls all other checks
    '''
    fileName = "data.csv"
    if df is None:
        df = pd.read_csv(fileName)
    missing_fields = check_fields(df)
    if missing_fields != None:
        return missing_fields
    # clean Student Id
    df = df[df.student_id > 0]
    df['student_id'] = df['student_id'].astype('int')

    # clean score
    # check the score is between 0 to 5
    df = df[(df.score > 0) & (df.score <= 5.0) ]

    # clean grade
    #check to see if Grade is valid list K thru 12
    df  = df.mask(lambda x : x['grade'].isin(valid_grades) )

    # clean test
    df["test"] = cleanTestData(df["test"])
    df = df[df.test != '']

    # clean district
    df['district'] = cleanDistrictData(df["district"])

    # clean duplicates
    # identify duplicate based on student id, grade and test
    df.drop_duplicates(['student_id','grade','test'],inplace=True)
    schema = processSchema(df)

    write_to_file('schmema.json',schema)

    return df


if __name__ == '__main__':
    df = data_import(None)
