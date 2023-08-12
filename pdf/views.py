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

def extract_subjects(subject):
    sub=subject.upper()
    sub=sub.split()
    return sub

# Create your views here.

def display(request):
    if request.method == "POST":

        sub_wise_data={}
        uploaded_file = request.FILES['document']
        subjects=request.POST.get("subject")
        subjects=extract_subjects(subjects)

        print(f"subjects typed are {subjects}")

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
        for sub in subjects:
            data=get_table_data(df,sub)
            sub_wise_data[sub]=data
            results=[]
            print(sub_wise_data)
        return render(request,"main.html",{"sub_wise_data":sub_wise_data,"columns":columns})



    
        
    return render(request,"main.html",{})
