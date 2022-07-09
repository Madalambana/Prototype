import time
import random
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
import models
from sqlalchemy import engine
from database import engine
from sqlalchemy.orm import Session
from database import get_db

def PID():
    return random.randrange(1000000) 


try:
    models.Base.metadata.create_all(bind=engine)
    print("Successfully Connected")
except Exception as error:
    print('error', error)

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

#Home page
@app.get("/")
def retunNothing():
    correctPage = RedirectResponse("/home")
    return correctPage

@app.get("/home", response_class=HTMLResponse)
def get(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, })


#Gender Based violence
@app.get("/vlg3nd37", response_class=HTMLResponse)
def get(request: Request):
    return templates.TemplateResponse("GBV.html", {"request": request})

@app.post("/vlg3nd37", response_class=HTMLResponse)
def get(request: Request, firstName: str = Form(...), lastName: str = Form(...),
  eth: str = Form(...),sex: str = Form(...),conNo: str = Form(...), pid: str = Form(...),
  report: str = Form(...),loc: str = Form(...), pos: str = Form(...), db: Session = Depends(get_db)):
    id = PID()
    gbv = models.GBV(pid = id, firstName = firstName, contact = conNo, report = report, 
    Id = pid, ethicinity = eth, lastName = lastName, gender = sex, location = loc, postal = pos)
    db.add(gbv)
    db.commit()
    db.refresh(gbv)
    return templates.TemplateResponse("success.html", {"request": request})

#Molest
@app.get("/vlm01357", response_class=HTMLResponse)
def get(request: Request):
    return templates.TemplateResponse("molest.html", {"request": request})

@app.post("/vlm01357", response_class=HTMLResponse)
def get(request: Request, firstName: str = Form(...),lastName: str = Form(...),
 eth: str = Form(...), conNo: str = Form(...),pid: str = Form(...),report: str = Form(...),
 loc: str = Form(...), pos: str = Form(...), db: Session = Depends(get_db) ):
    id = PID()
    molest = models.Molest(pid = id, firstName = firstName, lastName = lastName, contact = conNo,
    Id = pid, ethicinity = eth, report = report, location = loc, postal = pos)
    db.add(molest)
    db.commit()
    db.refresh(molest)
    return templates.TemplateResponse("success.html", {"request": request})

#Anonymity
@app.get("/vlan0nym17y", response_class=HTMLResponse)
def get(request: Request):
    return templates.TemplateResponse("anonymity.html", {"request": request})

@app.post("/vlan0nym17y", response_class=HTMLResponse)
def get(request: Request,Name: str = Form(...),
 conNo: str = Form(...), report: str = Form(...), loc: str = Form(...), pos: str = Form(...),
 db: Session = Depends(get_db) ):
    id = PID()
    anonymous = models.Assist(pid = id, firstName = Name, contact = conNo, report = report, location = loc,
    postal = pos)
    db.add(anonymous)
    db.commit()
    db.refresh(anonymous)
    return templates.TemplateResponse("success.html", {"request": request})

#about
@app.get("/about", response_class=HTMLResponse)
def get(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

#Contact
@app.get("/contact", response_class=HTMLResponse)
def get(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

#Developers
@app.get("/devs", response_class=HTMLResponse)
def get(request: Request):
    return templates.TemplateResponse("developers.html", {"request": request})
