# Dynamic Group QR Code Management System

This is a web application for managing WeChat group QR codes (also supports other group types), which can automatically switch and display QR codes for different groups when one group reaches its member limit.

[中文文档](README.md)

## Features

- Support uploading multiple WeChat group QR codes
- Dynamic QR code, never expired group QR code, permanent QR code
- Each group has two QR codes: original group QR code and permanent link QR code
- Admin backend to update group QR codes before groups reach capacity (TODO: Automatic switching to the next available group QR code)
- Provides both management and display interfaces
- Display page auto-refreshes to ensure QR codes are always up to date
- HTTPS support for secure access in production environment

The dynamic QR code functionality requires login for the admin backend, with username and password configured in the `.env` file. Each QR code's dedicated link can be accessed anonymously.

In the admin backend, each group displays two QR codes:
1. Original Group QR Code - The actual uploaded group QR code
2. Permanent Link QR Code - A permanent QR code pointing to the group's dedicated link, which can be used long-term

Configuration options in the .env file:
- URL_PREFIX=qrcode - URL prefix configuration
- PREFERRED_URL_SCHEME=https - URL scheme configuration (use https for production, http for local development)

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
   - Admin interface: http://localhost:5000/{qrcode}/group_adm_dna
   - Single QR code display interface: http://localhost:5000/group/xxxx

   Note: {qrcode} is the value configured in URL_PREFIX in the .env file, default is 'qrcode'

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