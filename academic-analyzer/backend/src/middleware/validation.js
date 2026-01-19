const Joi = require('joi');
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
    .pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/)
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
