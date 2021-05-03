from django.shortcuts import render

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt)
def index(request):
    # revisamos si es POST para poder trabajar los datos enviados
    if request.method == 'POST':
        dx = request.POST['dx']
        dy = request.POST['dy']
        with open('coordenadas.txt','w') as f:
            f.write('{"dx":' + dx + ', "dy":' + dy + '}')

    return render(request, 'pan_tilt/index.html')



def json(request):
    import json
    from django.http import JsonResponse
    with open('coordenadas.txt','r') as f:
        r = f.read()
        
        if r == "": return render(request, 'pan_tilt/json.html')
        
        print(r)
        data = json.loads(r)
        
    return JsonResponse(data)




