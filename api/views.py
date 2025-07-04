from django.shortcuts import redirect, render
from django.http import JsonResponse
from students.models import student
from .serializers import StudentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.
@api_view(['GET','POST'])
def students(request):
 if request.method == "GET":
    students = student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
 elif request.method =='POST':
   serializer =StudentSerializer(data=request.data)
   if serializer.is_valid():
     serializer.save()
     return Response(serializer.data, status=status.HTTP_201_CREATED)
   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
@api_view(['GET','Put'])
def studentsdetails(request, pk):
  try:
    students=student.objects.get(pk=pk)
  except student.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  if request.method == 'GET':
    serializer=StudentSerializer(students)
    return Response(serializer.data, status=status.HTTP_200_OK)
  elif request.method== 'PUT':
    serializer= StudentSerializer(students,data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def Student_login(request):
  if request.method == 'POST':
    username= request.POST['username']
    password= request.POST['password']
    conform_password= request.POST['conform_password']
    if password != conform_password:
      messages.error(request,"Password not match")
      return render(request,'signup.html')
    if User.objects.filter(username=username).exists():
      messages.error(request,"Username Alreaduy exists")
      return render(request,'signup.html')
    
    user= User.objects.create_user(username=username,password=password)
    messages.success(request,"User Create Successfully")
    return redirect('login')
  return render(request,'signup.html')  
      