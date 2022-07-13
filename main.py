import random
from fastapi import FastAPI, Request, Form, Depends, status,HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
import models, encrytion, schemas
from sqlalchemy import engine
from database import engine
from sqlalchemy.orm import Session
from database import get_db
from EV import settings
from oauth2 import create_access_token, current_user
from sqlalchemy import desc
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

def PID():
    return random.randrange(settings.RANGE) 

status = "pending"

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
    gbv = models.GBV(pid = id, firstName = firstName, contact = conNo, report = report, status = status,
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
    Id = pid, ethicinity = eth, report = report, location = loc, postal = pos, status = status)
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
    postal = pos, status = status)
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

##Admin section
#Signup
@app.get("/signup", response_class=HTMLResponse)
def get(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.post("/signup", response_class=HTMLResponse)
def sign_up(request: Request,username: str = Form(...),email: str = Form(...),  passwrd: str = Form(...),db: Session = Depends(get_db)):
    usernameQuery = db.query(models.Admins).filter(models.Admins.username == username).first()
    emailQuery = db.query(models.Admins).filter(models.Admins.email == email).first()
    if usernameQuery:
        return templates.TemplateResponse("error.html", {"request": request})
    if emailQuery:
        return templates.TemplateResponse("error.html", {"request": request})
    password = encrytion.encrypt(passwrd)
    passwrd = password
    newUser = models.Admins(username = username, email = email, password = passwrd)
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    redirect = RedirectResponse("/login")
    return redirect

#login
@app.get("/login", response_class=HTMLResponse)
def get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
def login(request: Request,username: str = Form(...), passwrd: str = Form(...)
 ,db: Session = Depends(get_db)):
    user = db.query(models.Admins).filter(models.Admins.username == username).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    if not encrytion.compare(passwrd, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=" Invalid credentials")
    access_token = create_access_token(data={"email": user.email})
    return templates.TemplateResponse("token_res.html", {"request": request,
     "AT": access_token, "TT": "bearer"}) 

#####################################################################################################
#postman automations
#Signup
@app.post("/signup+postman", )
def sign_up(postman: schemas.Signup,db: Session = Depends(get_db)):
    usernameQuery = db.query(models.Admins).filter(models.Admins.username == postman.username).first()
    emailQuery = db.query(models.Admins).filter(models.Admins.email == postman.email).first()
    if usernameQuery:
        return {"Username already exits "}
    if emailQuery:
        return {"Email already exits "}
    password = encrytion.encrypt(postman.password)
    postman.password = password
    newUser = models.Admins(**postman.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return {"Welcome aboard user:" : postman.username}

#login
@app.post("/login+postman")
def login(postman:OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):
    user = db.query(models.Admins).filter(models.Admins.username == postman.username).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    if not encrytion.compare(postman.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=" Invalid credentials")
    access_token = create_access_token(data={"email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

#solved
@app.get("/501v3d/gbv")
def allReports(db: Session = Depends(get_db),current_user: int = Depends(current_user)):
    security = db.query(models.Admins).filter(models.Admins.email == current_user.email).all()
    if not security:
        return {"access denied"}
    post = db.query(models.GBV).filter(models.GBV.status == "solved").all()
    return post

@app.get("/501v3d/molest")
def allReports(db: Session = Depends(get_db),current_user: int = Depends(current_user)):
    security = db.query(models.Admins).filter(models.Admins.email == current_user.email).all()
    if not security:
        return {"access denied"}
    post = db.query(models.Molest).filter(models.Molest.status == "solved").all()
    return post

@app.get("/501v3d/assist")
def allReports(db: Session = Depends(get_db),current_user: int = Depends(current_user)):
    security = db.query(models.Admins).filter(models.Admins.email == current_user.email).all()
    if not security:
        return {"access denied"}
    post = db.query(models.Assist).filter(models.Assist.status == "solved").all()
    return post

#pending
@app.get("/p3nd1ng/gbv")
def allReports(db: Session = Depends(get_db),current_user: int = Depends(current_user)):
    security = db.query(models.Admins).filter(models.Admins.email == current_user.email).all()
    if not security:
        return {"access denied"}
    post = db.query(models.GBV).filter(models.GBV.status == "pending").all()
    return post

@app.get("/p3nd1ng/molest")
def allReports(db: Session = Depends(get_db),current_user: int = Depends(current_user)):
    security = db.query(models.Admins).filter(models.Admins.email == current_user.email).all()
    if not security:
        return {"access denied"}
    post = db.query(models.Molest).filter(models.Molest.status == "pending").all()
    return post

@app.get("/p3nd1ng/assist")
def allReports(db: Session = Depends(get_db),current_user: int = Depends(current_user)):
    security = db.query(models.Admins).filter(models.Admins.email == current_user.email).all()
    if not security:
        return {"access denied"}
    post = db.query(models.Assist).filter(models.Assist.status == "solved").all()
    return post

#Deleting
@app.delete("/del/gbv/{id}")
def remove(id : int,db: Session = Depends(get_db),current_user: int = Depends(current_user)):
    security = db.query(models.Admins).filter(models.Admins.email == current_user.email).all()
    if not security:
        return {"access denied"}
    deletedPost = db.query(models.GBV).filter(models.GBV.pid == id)
    if deletedPost.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    deletedPost.delete(synchronize_session=False)
    db.commit()
    return "Successfully deleted"

@app.delete("/del/molest/{id}")
def remove(id : int,db: Session = Depends(get_db),current_user: int = Depends(current_user)):
    security = db.query(models.Admins).filter(models.Admins.email == current_user.email).all()
    if not security:
        return {"access denied"}
    deletedPost = db.query(models.Molest).filter(models.Molest.pid == id)
    if deletedPost.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    deletedPost.delete(synchronize_session=False)
    db.commit()
    return "Successfully deleted"

@app.delete("/del/assist/{id}")
def remove(id : int,db: Session = Depends(get_db),current_user: int = Depends(current_user)):
    security = db.query(models.Admins).filter(models.Admins.email == current_user.email).all()
    if not security:
        return {"access denied"}
    deletedPost = db.query(models.Assist).filter(models.Assist.pid == id)
    if deletedPost.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    deletedPost.delete(synchronize_session=False)
    db.commit()
    return "Successfully deleted"

#all reports from oldest to recent
#@app.get("/p3nd1ng/molest")
#def allReports(db: Session = Depends(get_db),): 
#    sort = db.query.order_by(desc(models.Molest.created_at)).all()
#    return sort