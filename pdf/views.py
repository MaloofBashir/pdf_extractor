from django.shortcuts import render
from django.http import HttpResponse
from docx import Document
import io
import pandas as pd
import docx
from tabulate import tabulate



table_data=[]

#This function will split the column1 or column2(subjects string) subjects into a list of suitable subject name
def split_column_subjects(subjects):
    sub_name=subjects.split("-")
    col_name=[ col.replace(" ","") for col in sub_name]
    subs_name=[col.replace("(" ,"") for col in col_name]
    col_name=[col.replace(")" ,"") for col in subs_name]
    return col_name

def get_table_data(df,sub_name,col_name):
    results=[]
    for index,row in df.iterrows():
        subjects=row[col_name]
        subjects_list=split_column_subjects(subjects)
        if sub_name in subjects_list:
            value=df.loc[index,"ClassRollNo"]
            if value.isdigit()!=True:
                results.append("--")
            
            results.append(value+",")
    return results

def extract_subjects(subject):
    sub=subject.upper()
    sub=sub.split()
    return sub


def reconstruct_dataframe(df):
    for index,row in df.iterrows():
        if (row["Name"]==""):
            new_sub1=df.loc[index-1,"Subjects1"]+df.loc[index,"Subjects1"]
            new_sub2=df.loc[index-1,"Subjects2"]+df.loc[index,"Subjects2"]
            df.loc[index-1,"Subjects1"]=new_sub1
            df.loc[index-1,"Subjects2"]=new_sub2
            new_df=df.dropna(subset=["Name"])
    df=df[df["Name"]!=""]
    df.reset_index(inplace=True)
    return df


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
            new_df=df.dropna(how='all')
            
            new_df=reconstruct_dataframe(new_df)
            print(new_df)
            
            # print(tabulate(new_df, headers='keys', tablefmt='pretty'))
            sub_wise_data = {}
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


