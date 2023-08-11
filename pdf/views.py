from django.shortcuts import render
from django.http import HttpResponse
from docx import Document
import io
import pandas as pd
import docx



table_data=[]
results=[]

def get_table_data(df,sub_name):
    for index,row in df.iterrows():
        value=row["Subjects1"]
        if sub_name in value:
            value=df.loc[index,"ClassRollNo"]
            if value.isdigit()!=True:
                print(df.iloc[index])
            
            results.append(value+",")
    return results

# Create your views here.

def display(request):
    if request.method == "POST":
        uploaded_file = request.FILES['document']
        file_content = uploaded_file.read()
        doc = Document(io.BytesIO(file_content))

    
        for table in doc.tables:
            # print("table is {table}")
            for row in table.rows:
                row_data=[]
                for cell in row.cells:
                    row_data.append(cell.text.strip())
                table_data.append(row_data)
        df=pd.DataFrame(table_data[1:],columns=table_data[0])
        columns=df.columns

        result=get_table_data(df,"ENG320")
        
        return render(request,"main.html",{"data":result,"columns":columns})



    
        
    return render(request,"main.html",{})
