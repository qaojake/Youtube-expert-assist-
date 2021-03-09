from collections import Counter

from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import os

from django.contrib import messages

import pandas as pd

# Create your views here.


#dict ={}
def index(request):

    context = {}
    global attribute

    if request.method == 'POST':

        uploaded_file = request.FILES['document']
        attribute = request.POST.get('attributeid')

        print(attribute)

        #check if this file ends with csv
        if uploaded_file.name.endswith('.csv'):
            savefile = FileSystemStorage()

            name = savefile.save(uploaded_file.name, uploaded_file) #gets the name of the file
            print(name)


            #we need to save the file somewhere in the project, MEDIA
            #now lets do the savings

            d = os.getcwd() # how we get the current dorectory
            file_directory = d+'\media\\'+name #saving the file in the media directory
            print(file_directory)
            readfile(file_directory)

            request.session['attribute'] = attribute

            if attribute not in data.axes[1]:
                messages.warning(request, 'Please write the column name correctly')
            else:
                print(attribute)
                return redirect(results)

        else:
            messages.warning(request, 'File was not uploaded. Please use .csv file extension!')


    return  render(request, 'index.html', context)


            #project_data.csv
def readfile(filename):

    #we have to create those in order to be able to access it around
    # use panda to read the file because i can use DATAFRAME to read the file
    #column;culumn2;column
    global rows,columns,data,my_file,missing_values
     #read the missing data - checking if there is a null
    missingvalue = ['?', '0', '--']

    my_file = pd.read_csv(filename, sep='[:;,|_]',na_values=missingvalue, engine='python')

    data = pd.DataFrame(data=my_file, index=None)
    print(data)

    rows = len(data.axes[0])
    columns = len(data.axes[1])


    null_data = data[data.isnull().any(axis=1)] # find where is the missing data #na null =['x1','x13']
    missing_values = len(null_data)



def results(request):
    # prepare the visualization
                                #12
    message = 'I found ' + str(rows) + ' rows and ' + str(columns) + ' columns. Missing data: ' + str(missing_values)
    messages.warning(request, message)

    dashboard = [] # ['A11','A11',A'122',]
    for x in data[attribute]:
        dashboard.append(x)

    my_dashboard = dict(Counter(dashboard)) #{'A121': 282, 'A122': 232, 'A124': 154, 'A123': 332}

    print(my_dashboard)

    keys = my_dashboard.keys() # {'A121', 'A122', 'A124', 'A123'}
    values = my_dashboard.values()

    listkeys = []
    listvalues = []

    for x in keys:
        listkeys.append(x)

    for y in values:
        listvalues.append(y)

    print(listkeys)
    print(listvalues)

    context = {
        'listkeys': listkeys,
        'listvalues': listvalues,
    }

    return render(request, 'result.html', context)
