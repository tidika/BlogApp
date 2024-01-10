from fastapi import APIRouter, Depends, HTTPException, Form, Request, applications
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db import get_db
from security import hash_password, check_password_hash

router = APIRouter()
templates = Jinja2Templates(directory="templates/auth")  # Assuming you have a 'templates' directory for HTML files


@router.post('/register', response_class=HTMLResponse)
async def register(request: Request, db: Session = Depends(get_db)):
    if request.method == 'POST':
        form = await request.form()
        username = form['username']
        password = form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, hash_password(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return RedirectResponse(url=app.url_path_for("auth:login"))

        # Use JSONResponse to send error messages
        return JSONResponse(content={'error': error}, status_code=400)

    return templates.TemplateResponse('auth/register.html', {'request': request})


@router.get('/login')
async def login_page(request: Request):
    return {"message": "This is the login page"}


@router.post('/login', response_class=HTMLResponse)
async def login(request: Request, db: Session = Depends(get_db), username: str = Form(...), password: str = Form(...)):
    # Handle POST request for login
    error = None
    user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

    if user is None:
        error = 'Incorrect username.'
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect password.'

    if error is None:
        # Implement your session or JWT logic here
        # Example: create a token, set a cookie, etc.
        return RedirectResponse(url=app.url_path_for("index"))  # Adjust the route as needed

    # Use JSONResponse to send error messages
    JSONResponse(content={'error': error}, status_code=400)

    return templates.TemplateResponse('auth/register.html', {'request': request})

# @router.get('/register', response_class=HTMLResponse)
# async def register_page(request: Request):
#     return templates.TemplateResponse("register.html", {"request": request})

# @router.post('/register', response_class=HTMLResponse)
# async def register(request: Request, db: Session = Depends(get_db), username: str = Form(...), password: str = Form(...)):
#     # Implement your registration logic here using the provided parameters
#     # Example: hash the password, store user details in the database, etc.
#     hashed_password = hash_password(password)
#     # Store user details in the database (you need to implement this function)

#     return templates.TemplateResponse("register_success.html", {"request": request, "username": username})


# @router.get('/login', response_class=HTMLResponse)
# async def login_page(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})


# @router.post('/login', response_class=HTMLResponse)
# async def login(request: Request, db: Session = Depends(get_db), username: str = Form(...), password: str = Form(...)):
#     # Implement your login logic here using the provided parameters
#     # Example: retrieve user details from the database, verify the password, etc.
#     # You need to implement functions like get_user_by_username and verify_password

#     # If login successful, set a session or JWT token
#     # Example: session['user_id'] = user.id or generate JWT token

#     return templates.TemplateResponse("login_success.html", {"request": request, "username": username})
