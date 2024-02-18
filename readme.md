python3 -m virtualenv env

cd env & source bin/activate #linux
cd env & script\activate #windows

start the app with parameter --app-dir
uvicorn.exe --app-dir .\product\ main:app --reload