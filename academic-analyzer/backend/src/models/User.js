const bcrypt = require('bcryptjs');

module.exports = (sequelize, DataTypes) => {
  const User = sequelize.define('User', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    email: {
      type: DataTypes.STRING,
      allowNull: false,
      unique: true,
      validate: {
        isEmail: {
          msg: 'Must be a valid email address'
        }
      }
    },
    password: {
      type: DataTypes.STRING,
      allowNull: false,
      validate: {
        len: {
          args: [8, 100],
          msg: 'Password must be at least 8 characters long'
        }
      }
    },
    firstName: {
      type: DataTypes.STRING,
      allowNull: false,
      validate: {
        len: {
          args: [1, 50],
          msg: 'First name must be between 1 and 50 characters'
        }
      }
    },
    lastName: {
      type: DataTypes.STRING,
      allowNull: false,
      validate: {
        len: {
          args: [1, 50],
          msg: 'Last name must be between 1 and 50 characters'
        }
      }
    },
    role: {
      type: DataTypes.ENUM('student', 'teacher', 'admin'),
      defaultValue: 'student',
      allowNull: false
    },
    isActive: {
      type: DataTypes.BOOLEAN,
      defaultValue: true
    },
    isVerified: {
      type: DataTypes.BOOLEAN,
      defaultValue: false
    },
    verificationToken: {
      type: DataTypes.STRING,
      allowNull: true
    },
    resetPasswordToken: {
      type: DataTypes.STRING,
      allowNull: true
    },
    resetPasswordExpires: {
      type: DataTypes.DATE,
      allowNull: true
    },
    lastLogin: {
      type: DataTypes.DATE,
      allowNull: true
    },
    loginAttempts: {
      type: DataTypes.INTEGER,
      defaultValue: 0
    },
    lockUntil: {
      type: DataTypes.DATE,
      allowNull: true
    }
  }, {
    tableName: 'users',
    timestamps: true,
    hooks: {
      beforeCreate: async (user) => {
        if (user.password) {
          const salt = await bcrypt.genSalt(10);
          user.password = await bcrypt.hash(user.password, salt);
        }
      },
      beforeUpdate: async (user) => {
        if (user.changed('password')) {
          const salt = await bcrypt.genSalt(10);
          user.password = await bcrypt.hash(user.password, salt);
        }
      }
    }
  });

  // Instance methods
  User.prototype.comparePassword = async function(candidatePassword) {
    return await bcrypt.compare(candidatePassword, this.password);
  };

  User.prototype.toJSON = function() {
    const values = Object.assign({}, this.get());
    delete values.password;
    delete values.verificationToken;
    delete values.resetPasswordToken;
    delete values.resetPasswordExpires;
    return values;
  };

  User.prototype.isLocked = function() {
    return !!(this.lockUntil && this.lockUntil > Date.now());
  };

  User.prototype.incrementLoginAttempts = async function() {
    // If previous lock has expired, reset attempts
    if (this.lockUntil && this.lockUntil < Date.now()) {
      return await this.update({
        loginAttempts: 1,
        lockUntil: null
      });
    }

    const updates = { loginAttempts: this.loginAttempts + 1 };

    // Lock account after 5 failed attempts for 2 hours
    if (this.loginAttempts + 1 >= 5 && !this.isLocked()) {
      updates.lockUntil = Date.now() + 2 * 60 * 60 * 1000; // 2 hours
    }

    return await this.update(updates);
  };

  User.prototype.resetLoginAttempts = async function() {
    return await this.update({
      loginAttempts: 0,
      lockUntil: null
    });
  };

  // Associations
  User.associate = (models) => {
    User.hasOne(models.StudentProfile, {
      foreignKey: 'userId',
      as: 'studentProfile',
      onDelete: 'CASCADE'
    });

    User.hasMany(models.Analysis, {
      foreignKey: 'userId',
      as: 'analyses',
      onDelete: 'CASCADE'
    });

    User.hasMany(models.RefreshToken, {
      foreignKey: 'userId',
      as: 'refreshTokens',
      onDelete: 'CASCADE'
    });
  };

  return User;
};
