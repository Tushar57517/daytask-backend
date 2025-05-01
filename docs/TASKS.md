# Tasks API Documentation

This document provides detailed information about the API endpoints related to task management in the application.

## Base URL

All task endpoints are prefixed with:

```
/api/tasks/
```

## Authentication

All task endpoints require authentication. Authentication is managed through JWT tokens.

## Available Endpoints

### 1. List Tasks

Retrieves all tasks that the authenticated user owns or is a member of.

- **URL**: `/api/tasks/list/`
- **Method**: `GET`
- **Authentication**: Required
- **Permissions**: Authenticated users only

#### Response

- **Status Code**: 200 OK
- **Content Type**: `application/json`
- **Body**:

```json
[
  {
    "id": 1,
    "title": "Complete Project",
    "desc": "Finish the backend implementation",
    "time": "14:00:00",
    "date": "2025-05-01",
    "created_at": "2025-04-29T10:00:00Z",
    "updated_at": "2025-04-29T10:00:00Z",
    "owner": "johndoe",
    "members_detail": ["janedoe", "marksmith"]
  },
  {
    "id": 2,
    "title": "Review Code",
    "desc": "Review pull request #42",
    "time": "10:00:00",
    "date": "2025-04-30",
    "created_at": "2025-04-28T15:30:00Z",
    "updated_at": "2025-04-28T15:30:00Z",
    "owner": "johndoe",
    "members_detail": ["janedoe"]
  }
]
```

### 2. Create Task

Creates a new task with the authenticated user as the owner.

- **URL**: `/api/tasks/create/`
- **Method**: `POST`
- **Authentication**: Required
- **Permissions**: Authenticated users only

#### Request

- **Content Type**: `application/json`
- **Body**:

```json
{
  "title": "New Task",
  "desc": "Task description here",
  "time": "09:00:00",
  "date": "2025-05-15",
  "members": ["janedoe", "marksmith"]
}
```

#### Response

- **Success**:
  - **Status Code**: 201 Created
  - **Content Type**: `application/json`
  - **Body**:
  ```json
  {
    "message": "task created successfully."
  }
  ```

- **Error**:
  - **Status Code**: 400 Bad Request
  - **Content Type**: `application/json`
  - **Body**:
  ```json
  {
    "title": ["This field is required."],
    "members": ["Invalid username: nonexistentuser"]
  }
  ```

### 3. Get Task Details

Retrieves details for a specific task.

- **URL**: `/api/tasks/<int:pk>/detail/`
- **Method**: `GET`
- **Authentication**: Required
- **Permissions**: Task owner or member only
- **URL Parameters**:
  - `pk`: ID of the task to retrieve

#### Response

- **Success**:
  - **Status Code**: 200 OK
  - **Content Type**: `application/json`
  - **Body**:
  ```json
  {
    "id": 1,
    "title": "Complete Project",
    "desc": "Finish the backend implementation",
    "time": "14:00:00",
    "date": "2025-05-01",
    "created_at": "2025-04-29T10:00:00Z",
    "updated_at": "2025-04-29T10:00:00Z", 
    "owner": "johndoe",
    "members_detail": ["janedoe", "marksmith"]
  }
  ```

- **Error** (Task Not Found):
  - **Status Code**: 404 Not Found
  - **Content Type**: `application/json`
  - **Body**:
  ```json
  {
    "setail": "task not found."
  }
  ```

- **Error** (Permission Denied):
  - **Status Code**: 403 Forbidden
  - **Content Type**: `application/json`
  - **Body**:
  ```json
  {
    "detail": "You do not have permission to view this task."
  }
  ```

### 4. Update Task

Updates an existing task.

- **URL**: `/api/tasks/<int:pk>/update/`
- **Method**: `PATCH`
- **Authentication**: Required
- **Permissions**: Task owner only
- **URL Parameters**:
  - `pk`: ID of the task to update

#### Request

- **Content Type**: `application/json`
- **Body** (partial update supported):

```json
{
  "title": "Updated Task Title",
  "desc": "Updated description",
  "members": ["newmember", "existingmember"]
}
```

#### Response

- **Success**:
  - **Status Code**: 200 OK
  - **Content Type**: `application/json`
  - **Body**:
  ```json
  {
    "id": 1,
    "title": "Updated Task Title",
    "desc": "Updated description",
    "time": "14:00:00",
    "date": "2025-05-01",
    "created_at": "2025-04-29T10:00:00Z",
    "updated_at": "2025-04-29T11:30:00Z",
    "owner": "johndoe",
    "members_detail": ["newmember", "existingmember"]
  }
  ```

- **Error** (Task Not Found):
  - **Status Code**: 404 Not Found
  - **Content Type**: `application/json`
  - **Body**:
  ```json
  {
    "message": "Task not found."
  }
  ```

- **Error** (Permission Denied):
  - **Status Code**: 403 Forbidden
  - **Content Type**: `application/json`
  - **Body**:
  ```json
  {
    "message": "You do not have permission to update this task."
  }
  ```

- **Error** (Validation Error):
  - **Status Code**: 400 Bad Request
  - **Content Type**: `application/json`
  - **Body**:
  ```json
  {
    "members": ["Invalid username: nonexistentuser"],
    "title": ["This field may not be blank."]
  }
  ```

### 5. Delete Task

Deletes a specific task.

- **URL**: `/api/tasks/<int:pk>/delete/`
- **Method**: `DELETE`
- **Authentication**: Required
- **Permissions**: Task owner only
- **URL Parameters**:
  - `pk`: ID of the task to delete

#### Response

- **Success**:
  - **Status Code**: 200 OK
  - **Content Type**: `application/json`
  - **Body**:
  ```json
  {
    "message": "Task deleted successfully."
  }
  ```

- **Error** (Task Not Found):
  - **Status Code**: 404 Not Found
  - **Content Type**: `application/json`
  - **Body**:
  ```json
  {
    "message": "Task not found."
  }
  ```

- **Error** (Permission Denied):
  - **Status Code**: 403 Forbidden
  - **Content Type**: `application/json`
  - **Body**:
  ```json
  {
    "message": "You do not have permission to delete this task."
  }
  ```

## Task Membership

Tasks can be assigned to multiple users:
- The task creator is always the owner
- The owner can add other users as members
- Only the task owner can update or delete the task
- Both owners and members can view the task details

## Error Handling

All endpoints return appropriate HTTP status codes and descriptive error messages in case of failure:

- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Authentication failed or not provided
- `403 Forbidden`: User does not have permission to perform the action
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

## Implementation Notes

- Tasks are associated with both an owner and potentially multiple members
- The task listing endpoint returns all tasks where the user is either an owner or a member
- Task members are specified by username in the API
- When creating or updating tasks with members, the API validates that all usernames exist
- Task serialization includes a read-only `members_detail` field that shows member usernames
