from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to Gym Booker! 🏋️‍♂️ Book your classes here.")

