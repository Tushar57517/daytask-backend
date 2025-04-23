# Authentication API Documentation

This document provides a comprehensive guide for the authentication endpoints in our Django REST API. All routes are prefixed with `/api/accounts/`.

## Table of Contents
- [Registration](#registration)
- [Email Verification](#email-verification)
- [Login](#login)
- [Token Refresh](#token-refresh)
- [Password Change](#password-change)
- [Password Reset Request](#password-reset-request)
- [Password Reset Confirmation](#password-reset-confirmation)
- [Logout](#logout)

## Registration

Register a new user account. A verification email will be sent to the provided email address.

- **URL:** `/api/accounts/register/`
- **Method:** `POST`
- **Authentication Required:** No

### Request Body
```json
{
  "name": "John Doe",
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

### Response

#### Success (200 OK)
```json
{
  "message": "verification link sent."
}
```

#### Error (400 Bad Request)
```json
{
  "email": ["This field must be unique."],
  "username": ["This field must be unique."]
}
```

## Email Verification

Verify a user's email address using the token sent to their email.

- **URL:** `/api/accounts/verify-email/`
- **Method:** `GET`
- **Authentication Required:** No
- **Query Parameters:** `token` (JWT token received in the verification email)

### Response

#### Success (200 OK)
```json
{
  "message": "email verified successfully"
}
```

#### Error (400 Bad Request)
```json
{
  "error": "invalid or expired token."
}
```

## Login

Authenticate a user and receive JWT tokens for authorization.

- **URL:** `/api/accounts/login/`
- **Method:** `POST`
- **Authentication Required:** No

### Request Body
```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

### Response

#### Success (200 OK)
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Error (400 Bad Request)
```json
{
  "non_field_errors": ["user not found!"]
}
```
or
```json
{
  "non_field_errors": ["email not verified"]
}
```
or
```json
{
  "non_field_errors": ["incorrect password"]
}
```

## Token Refresh

Obtain a new access token using a valid refresh token.

- **URL:** `/api/accounts/refresh/`
- **Method:** `POST`
- **Authentication Required:** No

### Request Body
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Response

#### Success (200 OK)
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Error (400 Bad Request)
```json
{
  "error": "Invalid or expired refresh token"
}
```
or
```json
{
  "message": "refresh token required."
}
```

## Password Change

Change the password for an authenticated user.

- **URL:** `/api/accounts/change-password/`
- **Method:** `POST`
- **Authentication Required:** Yes (Access token in Authorization header)

### Request Headers
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Request Body
```json
{
  "old_password": "currentsecurepassword",
  "new_password": "newsecurepassword123"
}
```

### Response

#### Success (200 OK)
```json
{
  "message": "Password changed successfully."
}
```

#### Error (400 Bad Request)
```json
{
  "old_password": ["Incorrect old password."]
}
```
or
```json
{
  "new_password": ["New password must be different from the old one."]
}
```
or
```json
{
  "new_password": ["This password is too common."]
}
```

## Password Reset Request

Request a password reset link to be sent to the user's email.

- **URL:** `/api/accounts/reset-password/`
- **Method:** `POST`
- **Authentication Required:** No

### Request Body
```json
{
  "email": "john@example.com"
}
```

### Response

#### Success (200 OK)
```json
{
  "message": "Password reset link sent to email"
}
```

#### Error (400 Bad Request)
```json
{
  "email": ["no account with this email found"]
}
```

## Password Reset Confirmation

Reset the password using the token received in the reset email.

- **URL:** `/api/accounts/reset-password-confirm/`
- **Method:** `POST`
- **Authentication Required:** No

### Request Body
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "new_password": "newsecurepassword123"
}
```

### Response

#### Success (200 OK)
```json
{
  "message": "Password reset successful"
}
```

#### Error (400 Bad Request)
```json
{
  "token": ["Invalid or expired token."]
}
```

## Logout

Invalidate a refresh token to logout a user.

- **URL:** `/api/accounts/logout/`
- **Method:** `POST`
- **Authentication Required:** Yes (Access token in Authorization header)

### Request Headers
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Request Body
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Response

#### Success (200 OK)
```json
{
  "message": "successfully logged out"
}
```

#### Error (400 Bad Request)
```json
{
  "error": "refresh token is required."
}
```
or
```json
{
  "error": "invalid token"
}
```

## Error Response Format

All API errors return a relevant HTTP status code along with a JSON response containing error details.

## Authentication

Most endpoints require authentication using JWT (JSON Web Tokens). To authenticate requests:

1. Obtain access and refresh tokens by logging in
2. Include the access token in the Authorization header of subsequent requests:
   ```
   Authorization: Bearer <access_token>
   ```
3. When the access token expires, use the refresh token to obtain a new access token.