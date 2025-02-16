# Dynamic Group QR Code Management System

This is a web application for managing WeChat group QR codes, which can automatically switch and display QR codes for different groups when one group reaches its member limit.

[中文文档](README.md)

## Features

- Support uploading multiple WeChat group QR codes
- Configurable maximum group member limit
- Dynamic QR code, never expired group QR code, permanent QR code
- Admin backend to update group QR codes before groups reach capacity (TODO: Automatic switching to the next available group QR code)
- Provides both management and display interfaces
- Display page auto-refreshes to ensure QR codes are always up to date

The dynamic QR code functionality requires login for the admin backend, with username and password configured in the `.env` file. Each QR code's dedicated link can be accessed anonymously.

A `URL_PREFIX=qrcode` configuration has been added to the `.env` file.

Flask Blueprint is used to implement URL prefix functionality.
All routes except `/group/<display_code>` are moved to the prefixed Blueprint.

All `url_for` calls have been updated to use the new Blueprint route names.

Current URL structure:
- `/qrcode/` - Redirects to admin backend
- `/qrcode/group_adm_dna` - Admin backend (login required)
- `/qrcode/login` - Login page
- `/qrcode/logout` - Logout
- `/group/<display_code>` - Display specific QR code (unchanged, no prefix)

## Interface Preview

### Login Interface
![Login Interface](/images/login.png)

### Admin Backend
![Admin Backend](/images/qrcode_admin.png)

## Installation

1. Ensure Python 3.10 or higher is installed
2. Clone this repository
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the application:
   ```bash
   python app.py
   ```

2. Open your browser and visit:
   - Admin interface: http://localhost:5000/qrcode/group_adm_dna
   - Display interface: http://localhost:5000/group/display

3. In the admin interface:
   - Upload new group QR codes
   - Set group names and maximum member limits
   - Set display order
   - Manage group member count (increase/decrease)
   - Delete unused QR codes

4. The display interface will automatically show the currently active group QR code and refresh every 60 seconds

## Notes

- Ensure uploaded QR code images are clear and usable
- Regularly check group member counts to ensure data accuracy
- Control QR code switching order by adjusting display order
- Recommend using fullscreen display for optimal viewing experience 