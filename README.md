
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


# Kindr

