from django.shortcuts import render
from django.http import HttpResponse
from docx import Document
import io
import pandas as pd
import docx
from tabulate import tabulate



table_data=[]

def get_table_data(df,sub_name,col_name):
    results=[]
    for index,row in df.iterrows():
        value=row[col_name]
        if index==2:
            exit
        if sub_name in value:
            value=df.loc[index,"ClassRollNo"]
            if value.isdigit()!=True:
                results.append("--")
            
            results.append(value+",")
    return results

def extract_subjects(subject):
    sub=subject.upper()
    sub=sub.split()
    return sub




# Create your views here.

def display(request):
    if request.method == "POST":
        try:
            uploaded_file = request.FILES['document']
            subjects = request.POST.get("subject")
            col_name=request.POST.get("col_name")
            subjects = extract_subjects(subjects)

            file_content = uploaded_file.read()
            doc = Document(io.BytesIO(file_content))

            table_data = []
            for table in doc.tables:
                for row in table.rows:
                    row_data = []
                    for cell in row.cells:
                        row_data.append(cell.text.strip())
                    table_data.append(row_data)
            df = pd.DataFrame(table_data[1:], columns=table_data[0])


            sub_wise_data = {}
            columns = df.columns
            for sub in subjects:
                data = get_table_data(df, sub,col_name)
                sub_wise_data[sub] = data

            error = ""  # Initialize error message
        except:
            error = "something went wrong"
            sub_wise_data = {}  # Clear the dictionary in case of an error

        return render(request, "main.html", {"sub_wise_data": sub_wise_data, "error": error})

    else:
        return render(request, "main.html", {"sub_wise_data": {}})


