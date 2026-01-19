# API Documentation

## Base URL
```
Development: http://localhost:5000/api
Production: https://api.academic-analyzer.com/api
```

## Authentication
All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

---

## Authentication Endpoints

### Register User
**POST** `/auth/register`

**Request Body:**
```json
{
  "email": "student@example.com",
  "password": "SecurePass123",
  "firstName": "John",
  "lastName": "Doe",
  "role": "student"
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": "uuid",
      "email": "student@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "role": "student"
    },
    "token": "jwt_token_here"
  }
}
```

### Login
**POST** `/auth/login`

**Request Body:**
```json
{
  "email": "student@example.com",
  "password": "SecurePass123"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "email": "student@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "role": "student"
    },
    "token": "jwt_access_token",
    "refreshToken": "jwt_refresh_token"
  }
}
```

### Refresh Token
**POST** `/auth/refresh`

**Request Body:**
```json
{
  "refreshToken": "your_refresh_token"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "token": "new_access_token"
  }
}
```

### Logout
**POST** `/auth/logout`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

## Analysis Endpoints

### Upload Answer Sheet
**POST** `/analysis/upload`

**Headers:** 
- `Authorization: Bearer <token>`
- `Content-Type: multipart/form-data`

**Form Data:**
- `file`: Answer sheet PDF/image
- `subject`: Subject name (string)
- `examType`: "midterm" | "final" | "quiz" | "mock"
- `totalMarks`: Total marks (optional)

**Response:** `201 Created`
```json
{
  "success": true,
  "message": "Analysis started",
  "data": {
    "analysisId": "uuid",
    "status": "processing",
    "estimatedTime": 30
  }
}
```

### Get Analysis by ID
**GET** `/analysis/:id`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "subject": "Mathematics",
    "examType": "midterm",
    "status": "completed",
    "createdAt": "2024-01-19T12:00:00Z",
    "results": {
      "scorePrediction": {
        "currentScore": 75.5,
        "potentialScore": 85.0,
        "maxScore": 100,
        "improvementPercentage": 12.6
      },
      "errorAnalyses": [
        {
          "questionNumber": 1,
          "errorTypes": ["Incomplete"],
          "severity": "Major",
          "specificErrors": [
            {
              "error": "Missing key concept",
              "location": "Step 2"
            }
          ]
        }
      ],
      "improvementSuggestions": [
        {
          "questionNumber": 1,
          "currentScore": 6,
          "potentialScore": 8,
          "improvements": [
            {
              "type": "add_concept",
              "detail": "Explain the Pythagorean theorem application",
              "impact": "+2 marks"
            }
          ],
          "priority": "High"
        }
      ],
      "studyRecommendations": [
        {
          "topic": "Geometry",
          "resourceType": "Video",
          "title": "Understanding Pythagorean Theorem",
          "url": "https://example.com/video",
          "difficulty": "Intermediate"
        }
      ]
    }
  }
}
```

### Get User's Analyses
**GET** `/analysis`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10)
- `subject`: Filter by subject
- `examType`: Filter by exam type

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "analyses": [...],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 25,
      "pages": 3
    }
  }
}
```

### Delete Analysis
**DELETE** `/analysis/:id`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Analysis deleted successfully"
}
```

---

## Student Profile Endpoints

### Get Profile
**GET** `/students/profile`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "userId": "uuid",
    "grade": "10",
    "school": "Springfield High",
    "subjects": ["Mathematics", "Physics", "Chemistry"],
    "performanceMetrics": {
      "averageScore": 78.5,
      "totalAnalyses": 15,
      "improvementRate": 12.3
    }
  }
}
```

### Update Profile
**PUT** `/students/profile`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "grade": "11",
  "school": "Springfield High",
  "subjects": ["Mathematics", "Physics", "Chemistry", "Biology"]
}
```

**Response:** `200 OK`

### Get Performance Metrics
**GET** `/students/performance`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `period`: "week" | "month" | "year" | "all"

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "period": "month",
    "metrics": {
      "totalTests": 8,
      "averageScore": 76.5,
      "highestScore": 92,
      "lowestScore": 65,
      "improvementTrend": 8.5,
      "subjectPerformance": [
        {
          "subject": "Mathematics",
          "averageScore": 78,
          "testsCount": 3
        }
      ],
      "weakAreas": [
        {
          "topic": "Calculus",
          "frequency": 5,
          "severity": "High"
        }
      ]
    }
  }
}
```

---

## Admin Endpoints

### Get All Users
**GET** `/admin/users`

**Headers:** `Authorization: Bearer <token>`

**Required Role:** `admin`

**Query Parameters:**
- `page`: Page number
- `limit`: Items per page
- `role`: Filter by role
- `search`: Search by name/email

**Response:** `200 OK`

### Get System Analytics
**GET** `/admin/analytics`

**Headers:** `Authorization: Bearer <token>`

**Required Role:** `admin`

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "totalUsers": 1250,
    "totalAnalyses": 5430,
    "activeUsers": 450,
    "avgProcessingTime": 25,
    "systemHealth": {
      "cpu": 45,
      "memory": 68,
      "database": "healthy",
      "aiServices": "healthy"
    }
  }
}
```

---

## Error Responses

### Validation Error (400)
```json
{
  "success": false,
  "message": "Validation failed",
  "errors": [
    {
      "field": "email",
      "message": "Must be a valid email address"
    }
  ]
}
```

### Unauthorized (401)
```json
{
  "success": false,
  "message": "Invalid authentication token"
}
```

### Forbidden (403)
```json
{
  "success": false,
  "message": "Insufficient permissions"
}
```

### Not Found (404)
```json
{
  "success": false,
  "message": "Resource not found"
}
```

### Internal Server Error (500)
```json
{
  "success": false,
  "message": "Internal server error"
}
```

---

## Rate Limiting

- **General endpoints:** 100 requests per 15 minutes
- **Auth endpoints:** 5 requests per 15 minutes
- **File upload:** 10 requests per hour

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```

---

## Webhooks (Coming Soon)

Subscribe to analysis completion events:

**POST** `/webhooks/subscribe`

```json
{
  "url": "https://your-app.com/webhook",
  "events": ["analysis.completed", "analysis.failed"]
}
```
