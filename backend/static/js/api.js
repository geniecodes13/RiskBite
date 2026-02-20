/**
 * RiskBite API Client
 * Main module for all backend API communication
 */

const API_BASE_URL = 'http://localhost:8000';

class RiskBiteAPI {
  /**
   * Health check
   */
  static async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      return await response.json();
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  }

  /**
   * Register a new user
   */
  static async register(email, password) {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Registration failed');
      }
      
      const data = await response.json();
      // Store user info in localStorage
      localStorage.setItem('user_id', data.user_id);
      localStorage.setItem('email', data.email);
      return data;
    } catch (error) {
      console.error('Registration failed:', error);
      throw error;
    }
  }

  /**
   * Login user with email and password
   */
  static async login(email, password) {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Login failed');
      }
      
      const data = await response.json();
      // Store user info in localStorage
      localStorage.setItem('user_id', data.user_id);
      localStorage.setItem('email', data.email);
      localStorage.setItem('logged_in', 'true');
      return data;
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  }

  /**
   * Google OAuth login redirect
   */
  static async initiateGoogleLogin() {
    try {
      window.location.href = `${API_BASE_URL}/auth/google/login`;
    } catch (error) {
      console.error('Google login redirect failed:', error);
      throw error;
    }
  }

  /**
   * Logout (clear session storage)
   */
  static logout() {
    localStorage.removeItem('user_id');
    localStorage.removeItem('email');
    localStorage.removeItem('logged_in');
  }

  /**
   * Check if user is logged in
   */
  static isLoggedIn() {
    return localStorage.getItem('logged_in') === 'true' && localStorage.getItem('user_id');
  }

  /**
   * Get current user ID
   */
  static getUserId() {
    return localStorage.getItem('user_id');
  }

  /**
   * Get current user email
   */
  static getUserEmail() {
    return localStorage.getItem('email');
  }

  /**
   * Scan a product label - Main scanning endpoint
   * @param {File} imageFile - The image file to scan
   * @param {Array} conditions - User health conditions (optional)
   * @param {Number} userId - User ID (optional)
   */
  static async scanProduct(imageFile, conditions = null, userId = null) {
    try {
      const formData = new FormData();
      formData.append('image', imageFile);
      
      if (conditions && conditions.length > 0) {
        formData.append('conditions', JSON.stringify(conditions));
      }
      
      if (userId) {
        formData.append('user_id', userId);
      }
      
      const response = await fetch(`${API_BASE_URL}/scan`, {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Scan failed');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Product scan failed:', error);
      throw error;
    }
  }

  /**
   * Parse health information from natural language text
   */
  static async parseHealth(text) {
    try {
      const response = await fetch(`${API_BASE_URL}/parse-health`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Health parsing failed');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Health parsing failed:', error);
      throw error;
    }
  }

  /**
   * Save health history for a user
   */
  static async saveHealthHistory(userId, healthData) {
    try {
      const response = await fetch(`${API_BASE_URL}/health/${userId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: healthData }),
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to save health history');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Save health history failed:', error);
      throw error;
    }
  }

  /**
   * Get health history for a user
   */
  static async getHealthHistory(userId) {
    try {
      const response = await fetch(`${API_BASE_URL}/health/${userId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to retrieve health history');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Get health history failed:', error);
      throw error;
    }
  }

  /**
   * Get recent scans for a user
   */
  static async getScans(userId) {
    try {
      const response = await fetch(`${API_BASE_URL}/scans/${userId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to retrieve scans');
      }

      return await response.json();
    } catch (error) {
      console.error('Get scans failed:', error);
      throw error;
    }
  }

  /**
   * Handle OAuth callback parameters
   */
  static handleOAuthCallback() {
    const params = new URLSearchParams(window.location.search);
    const userId = params.get('user_id');
    const email = params.get('email');
    const auth = params.get('auth');
    
    if (userId && email && auth === 'google') {
      localStorage.setItem('user_id', userId);
      localStorage.setItem('email', email);
      localStorage.setItem('logged_in', 'true');
      return { userId, email, auth };
    }
    
    return null;
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = RiskBiteAPI;
}
