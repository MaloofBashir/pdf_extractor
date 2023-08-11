from django.shortcuts import render
from django.http import HttpResponse
from docx import Document
import io
import pandas as pd
import docx



table_data=[]

# Create your views here.

def display(request):
    if request.method=="POST":
        uploaded_file=request.FILES['document']

        with uploaded_file.open("r") as file:
            
            file_content=file.read()
    
            print("file content: ", file_content)


        # doc_content=uploaded_file.read()
        # doc=Document(io.BytesIO(doc_content))
        # doc=Document(io.BytesIO(doc_content))
        # print(doc)


        # new_doc=doc.tables[1]
        # print(new_doc)
    
        # for table in doc.tables:
        #     # print("table is {table}")
        #     for row in table.rows:
        #         row_data=[]
        #         print(row)
        #         for cell in row.cells:
        #             row_data.append(cell.text.strip())
        #         table_data.append(row_data)
                # print(table_data)
        # df=pd.DataFrame(table_data[1:],columns=table_data[0])

        # print(df)
        
    return render(request,"main.html",{})
