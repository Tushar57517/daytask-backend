# Profiles API Documentation

This document provides detailed information about the API endpoints related to user profiles in the application.

## Base URL

All profile endpoints are prefixed with:

```
/api/profile/
```

## Authentication

All profile endpoints require authentication unless explicitly stated otherwise. Authentication is managed through JWT tokens.

## Available Endpoints

### 1. Get User Profile

Retrieves the authenticated user's profile information.

- **URL**: `/api/profile/me/`
- **Method**: `GET`
- **Authentication**: Required
- **Permissions**: Authenticated users only

#### Response

- **Status Code**: 200 OK
- **Content Type**: `application/json`
- **Body**:

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com"
}
```

### 2. Edit User Name

Updates the authenticated user's name.

- **URL**: `/api/profile/me/edit/name/`
- **Method**: `PATCH`
- **Authentication**: Required
- **Permissions**: Authenticated users only

#### Request

- **Content Type**: `application/json`
- **Body**:

```json
{
  "name": "New User Name"
}
```

#### Response

- **Success**:
  - **Status Code**: 200 OK
  - **Content Type**: `application/json`
  - **Body**:
  ```json
  {
    "message": "user's name updated successfully."
  }
  ```

- **Error**:
  - **Status Code**: 400 Bad Request
  - **Content Type**: `application/json`
  - **Body**:
  ```json
  {
    "name": ["Error message details"]
  }
  ```

### 3. Request Email Update

Initiates the process to change the user's email address. This saves the new email as a pending email and sends a confirmation link to the new address.

- **URL**: `/api/profile/me/edit/email/`
- **Method**: `PATCH`
- **Authentication**: Required
- **Permissions**: Authenticated users only

#### Request

- **Content Type**: `application/json`
- **Body**:

```json
{
  "new_email": "new.email@example.com"
}
```

#### Response

- **Success**:
  - **Status Code**: 200 OK
  - **Content Type**: `application/json`
  - **Body**:
  ```json
  {
    "message": "Confirmation email sent."
  }
  ```

- **Error**:
  - **Status Code**: 400 Bad Request
  - **Content Type**: `application/json`
  - **Body**:
  ```json
  {
    "new_email": ["This email is already in use."]
  }
  ```

### 4. Confirm Email Update

Confirms the email address change after the user clicks the confirmation link sent to their new email. Updates the user's primary email and clears the pending email field.

- **URL**: `/api/profile/me/edit/email/confirm/`
- **Method**: `GET`
- **Authentication**: Not required (authentication is handled via token in query parameters)
- **Query Parameters**:
  - `token`: JWT token for authentication
  - `email`: New email address to confirm

#### Response

- **Success**:
  - **Status Code**: 200 OK
  - **Content Type**: `application/json`
  - **Body**:
  ```json
  {
    "message": "Email updated successfully."
  }
  ```

- **Error** (Invalid Token):
  - **Status Code**: 400 Bad Request
  - **Content Type**: `application/json`
  - **Body**:
  ```json
  {
    "error": "Invalid or expired token."
  }
  ```

- **Error** (Missing Parameters):
  - **Status Code**: 400 Bad Request
  - **Content Type**: `application/json`
  - **Body**:
  ```json
  {
    "error": "Missing token or email."
  }
  ```

- **Error** (User Not Found):
  - **Status Code**: 404 Not Found
  - **Content Type**: `application/json`
  - **Body**:
  ```json
  {
    "error": "User not found."
  }
  ```

- **Error** (Email Mismatch):
  - **Status Code**: 400 Bad Request
  - **Content Type**: `application/json`
  - **Body**:
  ```json
  {
    "error": "No pending email match."
  }
  ```

## Integration with Accounts System

The profiles API works in conjunction with the accounts system, which handles:
- User registration with email verification
- Login authentication
- Password change
- Password reset

## Email Verification Process

The application implements a secure email change process:
1. User requests an email change
2. The new email is stored as `pending_email` in the user model
3. A confirmation email with a token is sent to the new address
4. User confirms by clicking the link with the token
5. Upon successful verification, the email is updated and `pending_email` is cleared

## Error Handling

All endpoints return appropriate HTTP status codes and descriptive error messages in case of failure:

- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Authentication failed or not provided
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

## Implementation Notes

- JWT tokens are used for both authentication and for email confirmation
- All profile operations require the user to be authenticated and active
- The email confirmation system uses the same token mechanism as the account verification process
