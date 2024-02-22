### In order to run the code please follow the instruction below

```
Create the Virtual Env in python
python3 -m virtualenv env

Active the Virtual Env
#linux
cd env & source bin/activate 

#windows
cd env & script\activate 

Start the App (start the app with parameter --app-dir
uvicorn.exe --app-dir .\product\ main:app --reload
```