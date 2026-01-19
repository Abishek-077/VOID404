#!/usr/bin/env python3
"""
Academic Analyzer - Complete Project File Generator
This script creates all necessary source files for the project
"""

import os
import sys

BASE_PATH = "/home/claude/academic-analyzer"

def ensure_dir(filepath):
    """Ensure directory exists for filepath"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

def create_file(filepath, content):
    """Create file with content"""
    ensure_dir(filepath)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Created: {filepath.replace(BASE_PATH, '')}")

def generate_all_files():
    """Generate all project files"""
    
    files = {}
    
    # ========================================================================
    # BACKEND MIDDLEWARE
    # ========================================================================
    
    files[f"{BASE_PATH}/backend/src/middleware/auth.js"] = '''const jwt = require('jsonwebtoken');
const { User } = require('../models');
const logger = require('../utils/logger');

/**
 * Verify JWT token and attach user to request
 */
const auth = async (req, res, next) => {
  try {
    // Get token from header
    const token = req.header('Authorization')?.replace('Bearer ', '');

    if (!token) {
      return res.status(401).json({
        success: false,
        message: 'No authentication token provided'
      });
    }

    // Verify token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);

    // Find user
    const user = await User.findByPk(decoded.id);

    if (!user) {
      return res.status(401).json({
        success: false,
        message: 'User not found'
      });
    }

    if (!user.isActive) {
      return res.status(403).json({
        success: false,
        message: 'Account has been deactivated'
      });
    }

    // Attach user to request
    req.user = user;
    next();
  } catch (error) {
    logger.logSecurity('auth_failed', { error: error.message }, req);
    
    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({
        success: false,
        message: 'Token expired',
        code: 'TOKEN_EXPIRED'
      });
    }

    return res.status(401).json({
      success: false,
      message: 'Invalid authentication token'
    });
  }
};

/**
 * Check if user has required role
 */
const authorize = (...roles) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({
        success: false,
        message: 'Authentication required'
      });
    }

    if (!roles.includes(req.user.role)) {
      logger.logSecurity('unauthorized_access', {
        userId: req.user.id,
        role: req.user.role,
        requiredRoles: roles,
        path: req.path
      }, req);

      return res.status(403).json({
        success: false,
        message: 'Insufficient permissions'
      });
    }

    next();
  };
};

module.exports = { auth, authorize };
'''

    files[f"{BASE_PATH}/backend/src/middleware/errorHandler.js"] = '''const logger = require('../utils/logger');

/**
 * Not Found Middleware
 */
const notFound = (req, res, next) => {
  const error = new Error(`Not Found - ${req.originalUrl}`);
  error.statusCode = 404;
  next(error);
};

/**
 * Global Error Handler
 */
const errorHandler = (err, req, res, next) => {
  logger.logError(err, req);

  const statusCode = err.statusCode || err.status || 500;
  const message = err.message || 'Internal Server Error';

  // Sequelize validation errors
  if (err.name === 'SequelizeValidationError') {
    const errors = err.errors.map(e => ({
      field: e.path,
      message: e.message
    }));
    
    return res.status(400).json({
      success: false,
      message: 'Validation error',
      errors
    });
  }

  // Sequelize unique constraint errors
  if (err.name === 'SequelizeUniqueConstraintError') {
    return res.status(409).json({
      success: false,
      message: 'Resource already exists',
      field: err.errors[0]?.path
    });
  }

  // JWT errors
  if (err.name === 'JsonWebTokenError') {
    return res.status(401).json({
      success: false,
      message: 'Invalid token'
    });
  }

  if (err.name === 'TokenExpiredError') {
    return res.status(401).json({
      success: false,
      message: 'Token expired',
      code: 'TOKEN_EXPIRED'
    });
  }

  // Multer errors (file upload)
  if (err.name === 'MulterError') {
    if (err.code === 'LIMIT_FILE_SIZE') {
      return res.status(400).json({
        success: false,
        message: 'File too large'
      });
    }
    
    return res.status(400).json({
      success: false,
      message: 'File upload error'
    });
  }

  // Default error response
  res.status(statusCode).json({
    success: false,
    message,
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
};

module.exports = { notFound, errorHandler };
'''

    files[f"{BASE_PATH}/backend/src/middleware/validation.js"] = '''const Joi = require('joi');
const logger = require('../utils/logger');

/**
 * Validate request using Joi schema
 */
const validate = (schema, property = 'body') => {
  return (req, res, next) => {
    const { error, value } = schema.validate(req[property], {
      abortEarly: false,
      stripUnknown: true
    });

    if (error) {
      const errors = error.details.map(detail => ({
        field: detail.path.join('.'),
        message: detail.message
      }));

      logger.logSecurity('validation_failed', {
        errors,
        path: req.path
      }, req);

      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors
      });
    }

    req[property] = value;
    next();
  };
};

// Registration schema
const registrationSchema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().min(8).required()
    .pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)/)
    .message('Password must contain at least one uppercase, one lowercase, and one number'),
  firstName: Joi.string().min(1).max(50).required(),
  lastName: Joi.string().min(1).max(50).required(),
  role: Joi.string().valid('student', 'teacher').default('student')
});

// Login schema
const loginSchema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().required()
});

// Analysis upload schema
const analysisSchema = Joi.object({
  subject: Joi.string().min(1).max(100).required(),
  examType: Joi.string().valid('midterm', 'final', 'quiz', 'mock').required(),
  totalMarks: Joi.number().integer().min(1).max(1000).optional()
});

module.exports = {
  validate,
  validateRegistration: validate(registrationSchema),
  validateLogin: validate(loginSchema),
  validateAnalysis: validate(analysisSchema)
};
'''

    # ========================================================================
    # FRONTEND FILES
    # ========================================================================
    
    files[f"{BASE_PATH}/frontend/package.json"] = '''{
  "name": "academic-analyzer-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "@emotion/react": "^11.11.1",
    "@emotion/styled": "^11.11.0",
    "@mui/material": "^5.15.0",
    "@mui/icons-material": "^5.15.0",
    "@reduxjs/toolkit": "^2.0.1",
    "@testing-library/jest-dom": "^6.1.5",
    "@testing-library/react": "^14.1.2",
    "@testing-library/user-event": "^14.5.1",
    "axios": "^1.6.2",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-redux": "^9.0.4",
    "react-router-dom": "^6.20.1",
    "react-scripts": "5.0.1",
    "recharts": "^2.10.3",
    "react-dropzone": "^14.2.3",
    "react-pdf": "^7.6.0",
    "typescript": "^5.3.3",
    "web-vitals": "^3.5.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject",
    "lint": "eslint src/**/*.{ts,tsx}",
    "lint:fix": "eslint src/**/*.{ts,tsx} --fix"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  },
  "devDependencies": {
    "@types/react": "^18.2.45",
    "@types/react-dom": "^18.2.18",
    "@types/node": "^20.10.5",
    "eslint": "^8.55.0"
  }
}
'''

    files[f"{BASE_PATH}/frontend/tsconfig.json"] = '''{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "baseUrl": "src"
  },
  "include": ["src"]
}
'''

    # Create all files
    for filepath, content in files.items():
        create_file(filepath, content)
    
    print(f"\n🎉 Successfully created {len(files)} files!")

if __name__ == "__main__":
    try:
        generate_all_files()
        print("\n✅ All files generated successfully!")
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
