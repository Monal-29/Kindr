
# Kindr - Help & Donate Platform

A full-stack web application that connects people who need help with those who want to donate. Features include user authentication, help request creation, Tinder-like swipe interface, and admin verification system.

## Features

- **User Authentication**: Login and signup for donors, recipients, and admins
- **Help Requests**: Recipients can create help requests with documents
- **Swipe Interface**: Donors can swipe through verified help requests (like Tinder)
- **Admin Verification**: Admins can verify help requests with document review
- **Matches**: Track matches between donors and recipients

## Project Structure

```
kindr/
├── frontend/              # Frontend files
│   ├── css/              # Stylesheets
│   │   ├── styles.css
│   │   ├── auth-styles.css
│   │   ├── swipe-styles.css
│   │   └── landing-styles.css
│   ├── js/               # JavaScript files
│   │   ├── config.js     # API configuration
│   │   ├── auth.js       # Authentication handlers
│   │   └── swipe.js      # Swipe functionality
│   ├── index.html        # Landing page
│   ├── login.html        # Login page
│   ├── signup.html       # Signup page
│   ├── donor-dashboard.html
│   ├── recipient-dashboard.html
│   ├── admin-dashboard.html
│   ├── swipe.html        # Swipe interface
│   ├── matches.html      # Matches page
│   └── server.js         # Frontend server
└── backend/              # Backend files
    ├── routes/           # API routes
    │   ├── auth.py
    │   ├── help_requests.py
    │   ├── swipes.py
    │   ├── admin.py
    │   ├── donors.py
    │   └── recipients.py
    ├── database.py       # Database setup
    ├── middleware.py     # Authentication middleware
    ├── app.py            # Main Flask application
    ├── requirements.txt  # Python dependencies
    ├── kindr.db          # SQLite database (created on first run)
    └── uploads/          # Document uploads folder
```

## Setup Instructions

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Initialize database:**
   ```bash
   python database.py
   ```
   This will create the SQLite database and a default admin user:
   - Email: `admin@kindr.com`
   - Password: `admin123`

6. **Run the backend server:**
   ```bash
   python app.py
   ```
   The backend will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Start the frontend server:**
   ```bash
   node server.js
   ```
   The frontend will be available at `http://localhost:8000`

   **Alternative:** You can use Python's HTTP server:
   ```bash
   python -m http.server 8000
   ```

## Usage

### Default Admin Account
- **Email:** admin@kindr.com
- **Password:** admin123

### User Types

1. **Recipients**: Can create help requests that need to be verified by admin
2. **Donors**: Can swipe through verified help requests and match with recipients
3. **Admin**: Can verify/reject help requests and view statistics

### Workflow

1. **Sign Up**: Create an account as either a donor or recipient
2. **Login**: Login with your credentials
3. **For Recipients**:
   - Create a help request with title, description, category, and optional document
   - Wait for admin verification
   - View your requests and matches
4. **For Donors**:
   - Go to swipe page
   - Swipe right (like) or left (pass) on help requests
   - View your matches
5. **For Admins**:
   - View pending requests
   - Review documents
   - Verify or reject requests
   - View statistics

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login user
- `POST /api/auth/register` - Register new user

### Help Requests
- `POST /api/help-requests` - Create help request (recipients only)
- `GET /api/help-requests/verified` - Get verified requests (for swiping)
- `GET /api/help-requests/my-requests` - Get user's requests
- `GET /api/help-requests/:id` - Get specific request

### Swipes
- `POST /api/swipes` - Record swipe action
- `GET /api/swipes/matches` - Get user's matches

### Admin
- `GET /api/admin/pending-requests` - Get pending requests
- `POST /api/admin/verify-request/:id` - Verify/reject request
- `GET /api/admin/document/:id` - Download document
- `GET /api/admin/stats` - Get statistics

## Technologies Used

- **Backend**: Python, Flask, SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: JWT tokens
- **Database**: SQLite

## Notes

- The database file (`kindr.db`) will be created automatically on first run
- Document uploads are stored in the `backend/uploads/` directory
- All passwords are hashed using bcrypt
- JWT tokens expire after 24 hours

## Development

To run both servers simultaneously:
1. Open two terminal windows
2. Run backend in one: `cd backend && python app.py`
3. Run frontend in the other: `cd frontend && node server.js`

## License

This project is open source and available for educational purposes.

# Kindr

