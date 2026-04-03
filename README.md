# err0rgod Auth System

A modern, secure, and modular authentication system built with **Flask** and **JWT (JSON Web Tokens)**. This project demonstrates industry-standard practices for user registration, secure login, and session management.

## 🚀 Features

- **JWT-Based Authentication**: Uses `flask-jwt-extended` for secure, stateless user identities stored in **HTTP-only Cookies** (protects against XSS).
- **Professional Hashing**: Passwords are never stored in plain text; they are hashed using **Bcrypt** before saving to the database.
- **Real-time Validation**: Frontend JavaScript instantly validates password strength (uppercase, numbers, symbols) as the user types.
- **SQLite Database**: A persistent relational database for user storage.
- **Modular Blueprints**: Clean project structure separating `login` and `register` into independent modules.
- **Route Protection**: Custom `@jwt_required()` decorators and automated redirects for unauthorized users.

## 📂 Project Structure

```text
auth/
├── app.py              # Main entry point & JWT configuration
├── data/
│   ├── data.db         # SQLite database file
│   └── data_check.py   # Database initialization logic
├── login/
│   ├── login.py        # Login logic & token generation
│   └── templates/      # Login-specific HTML
├── register/
│   ├── register.py     # Registration logic & password hashing
│   └── templates/      # Registration-specific HTML
├── static/
│   └── css/            # Global styles
└── templates/          # Shared HTML (base, index, profile)
```

## 🛠️ Tech Stack

- **Backend**: Python 3.x, Flask
- **Security**: Flask-JWT-Extended, Bcrypt
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

## ⚙️ How it Works

### 1. Registration Flow
- **Frontend**: As the user types, a `keyup` event listener in `register.html` checks the password against multiple regex patterns. The "Sign Up" button remains disabled until all criteria are met.
- **Backend**: `register.py` receives the username and password. It checks if the username already exists in `data.db`. If unique, it hashes the password using `bcrypt.hashpw` and stores it.

### 2. Login & JWT Flow
- **Verification**: `login.py` fetches the hashed password from the database and verifies it using `bcrypt.checkpw`.
- **Token Generation**: Upon success, a JWT is created containing the user's identity.
- **Cookie Security**: The token is sent to the browser using `set_access_cookies`. It is marked as `HttpOnly`, meaning it cannot be accessed by client-side scripts (preventing XSS attacks).

### 3. Session Management
- **Context Processor**: In `app.py`, a `@app.context_processor` automatically detects the JWT in the browser's cookies. This makes the `current_user` available to all Jinja templates without manual passing.
- **Route Protection**: Routes like `/profile` are wrapped in `@jwt_required()`. If a user attempts to access them without a valid token, they are automatically redirected to the login page.

## 🏁 Setup & Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/err0rgod/auth.git
   cd auth
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the Database**:
   The database will automatically initialize itself the first time you run the app.

4. **Run the Application**:
   ```bash
   flask run --reload
   ```

---
*Created by [err0rgod](https://github.com/err0rgod)*
