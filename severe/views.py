from django.shortcuts import render, redirect
from django.http import HttpResponse
import pickle
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserCreationForm

def say_hello(request):
    #return HttpResponse('Hello World')  
    return render(request, 'index.html', {'name': 'Sydney'})

def home(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username = username, password=password)
            auth_login(request, user)
            return redirect('home')
    
    else:
        form = UserCreationForm()


    return render(request, 'registration/register.html', {'form':form})

def login(request):
    form = UserCreationForm()
    return render(request, 'registration/login.html', {'form': form})

def getClassifier(RPC_X_kin, RPC_Y_kin, RPC_Z_kin, RPC_U_kin, RPC_X_rest, RPC_Y_rest, RPC_Z_rest, RPC_U_rest, TSI_kin, TSI_amplitude_kin, Mean_Peak_Amplitude_kin, Stddev_Peak_Amplitude_kin, TSI_rest, TSI_amplitude_rest, Mean_Peak_Amplitude_rest, Stddev_Peak_Amplitude_rest):
    model = pickle.load(open('tremor_classifier_model.joblib', 'rb'))
    scaled = pickle.load(open('scaler.sav', 'rb'))
    # ['RPC_X_kin',
    #  'RPC_Y_kin',
    #  'RPC_Z_kin',
    #  'RPC_U_kin',
    #  'RPC_X_rest',
    #  'RPC_Y_rest',
    #  'RPC_Z_rest',
    #  'RPC_U_rest',
    #  'TSI_kin',
    #  'TSI_amplitude_kin',
    #  'Mean Peak Amplitude_kin',
    #  'Stddev Peak Amplitude_+kin',
    #  'TSI_rest',
    #  'TSI_amplitude_rest',
    #  'Mean Peak Amplitude_rest',
    #  'Stddev Peak Amplitude_+rest']

    prediction = model.predict(scaled.transform([
        [RPC_X_kin, RPC_Y_kin, RPC_Z_kin, RPC_U_kin, RPC_X_rest, RPC_Y_rest, RPC_Z_rest, RPC_U_rest, TSI_kin, TSI_amplitude_kin,
            Mean_Peak_Amplitude_kin, Stddev_Peak_Amplitude_kin, TSI_rest, TSI_amplitude_rest, Mean_Peak_Amplitude_rest, Stddev_Peak_Amplitude_rest]
    ]))
    
    if prediction == 0:
        return 'yes'
    elif prediction == 1:
        return 'no'
    else:
        return 'error'

def result(request):
    RPC_X_kin = float(request.GET['RPC_X_kin'])
    RPC_Y_kin = float(request.GET['RPC_Y_kin'])
    RPC_Z_kin = float(request.GET['RPC_Z_kin'])
    RPC_U_kin = float(request.GET['RPC_U_kin'])
    RPC_X_rest = float(request.GET['RPC_X_rest'])
    RPC_Y_rest = float(request.GET['RPC_Y_rest'])
    RPC_Z_rest = float(request.GET['RPC_Z_rest'])
    RPC_U_rest = float(request.GET['RPC_U_rest'])
    TSI_kin = float(request.GET['TSI_kin'])
    TSI_amplitude_kin = float(request.GET['TSI_amplitude_kin'])
    Mean_Peak_Amplitude_kin = float(request.GET['Mean_Peak_Amplitude_kin'])
    Stddev_Peak_Amplitude_kin = float(request.GET['Stddev_Peak_Amplitude_kin'])
    TSI_rest = float(request.GET['TSI_rest'])
    TSI_amplitude_rest = float(request.GET['TSI_amplitude_rest'])
    Mean_Peak_Amplitude_rest = float(request.GET['Mean_Peak_Amplitude_rest'])
    Stddev_Peak_Amplitude_rest = float(request.GET['Stddev_Peak_Amplitude_rest'])

    result = getClassifier(RPC_X_kin, RPC_Y_kin, RPC_Z_kin, RPC_U_kin, RPC_X_rest, RPC_Y_rest, RPC_Z_rest, RPC_U_rest, TSI_kin, TSI_amplitude_kin,
                           Mean_Peak_Amplitude_kin, Stddev_Peak_Amplitude_kin, TSI_rest, TSI_amplitude_rest, Mean_Peak_Amplitude_rest, Stddev_Peak_Amplitude_rest)

    return render(request, 'result.html', {'result': result})