Here's a structured README documentation for your QR Code File Downloader project:

---

# QR Code File Downloader

**QR Code File Downloader** is a web application that allows users to upload files and download them using QR codes. Users can also download the QR code image for their uploaded files. This project aims to simplify file sharing through QR codes, making it easy for users to access their files quickly.

## Table of Contents

- [QR Code File Downloader](#qr-code-file-downloader)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [API Endpoints](#api-endpoints)
    - [File Upload](#file-upload)
    - [File Download](#file-download)
    - [QR Code Download](#qr-code-download)
    - [User Authentication](#user-authentication)
      - [User Signup](#user-signup)
      - [User Login](#user-login)
      - [Refresh User Token](#refresh-user-token)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)

## Features

- **File Upload**: Users can upload their files securely.
- **File Download**: Authenticated users can download their uploaded files.
- **QR Code Generation**: A unique QR code is generated for each uploaded file, allowing easy access.
- **QR Code Download**: Users can download the QR code image to share their files quickly.
- **User Authentication**: Secure signup and login for users.

## API Endpoints

### File Upload

- **Endpoint**: `/doc/upload-file`
- **Method**: `POST`
- **Description**: Allows users to upload a file.

### File Download

- **Endpoint**: `/doc/download/file/{file_id}`
- **Method**: `GET`
- **Description**: Authenticated users can download their uploaded files.
- **Parameters**:
  - `file_id`: The unique identifier of the file to be downloaded.

### QR Code Download

- **Endpoint**: `/doc/download/qrcode/{qrcode_id}`
- **Method**: `GET`
- **Description**: Allows users to download the QR code image for their uploaded file.
- **Parameters**:
  - `qrcode_id`: The unique identifier of the QR code.

### User Authentication

#### User Signup

- **Endpoint**: `/auth/user/signup`
- **Method**: `POST`
- **Description**: Allows users to sign up for an account.
- **Body Parameters**:
  - `email`: User's email (type: `str`)
  - `password`: User's password (type: `str`)

#### User Login

- **Endpoint**: `/auth/user/login`
- **Method**: `POST`
- **Description**: Allows users to log in to their account.
- **Body Parameters**:
  - `email`: User's email (type: `str`)
  - `password`: User's password (type: `str`)

#### Refresh User Token

- **Endpoint**: `/auth/user/refresh-token`
- **Method**: `POST`
- **Description**: Allows users to refresh their authentication token.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd qr-code-file-downloader
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your environment variables (if any).

4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## Usage

1. **Sign Up**: Create an account using the signup endpoint.
2. **Log In**: Authenticate your account using the login endpoint.
3. **Upload a File**: Use the upload-file endpoint to upload your file.
4. **Download Your File**: Use the download endpoint with your file ID to download your uploaded file.
5. **Download QR Code**: Use the QR code download endpoint with your QR code ID to get the QR code image.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs or suggestions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to customize any sections to better fit your project's specifics or add any additional details as needed!
