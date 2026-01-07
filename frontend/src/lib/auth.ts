import { createAuthClient } from 'better-auth/react';
import { apiClient } from './api';

// Initialize Better Auth client
export const authClient = createAuthClient({
  baseURL: process.env.BETTER_AUTH_URL || 'http://localhost:8080',
  fetchOptions: {
    // Add any custom fetch options if needed
  },
});

// Session management functions
const SESSION_KEY = 'auth_session';

// Store session data
export const storeSession = (userData: any, token: string) => {
  const sessionData = {
    user: userData,
    token,
    timestamp: Date.now(),
  };
  localStorage.setItem(SESSION_KEY, JSON.stringify(sessionData));
  apiClient.setToken(token);
};

// Retrieve session data
export const getSession = () => {
  const sessionData = localStorage.getItem(SESSION_KEY);
  if (sessionData) {
    try {
      return JSON.parse(sessionData);
    } catch (error) {
      console.error('Error parsing session data:', error);
      return null;
    }
  }
  return null;
};

// Clear session data
export const clearSession = () => {
  localStorage.removeItem(SESSION_KEY);
  apiClient.clearToken();
};

// Validate session (check if it's expired)
export const isValidSession = () => {
  const session = getSession();
  if (!session) return false;

  // Check if session is older than 24 hours (86400000 ms)
  const now = Date.now();
  const sessionAge = now - session.timestamp;
  const maxAge = 24 * 60 * 60 * 1000; // 24 hours in milliseconds

  if (sessionAge > maxAge) {
    clearSession();
    return false;
  }

  return true;
};

// Export authentication methods
export const signIn = async (email: string, password: string) => {
  try {
    // Use our API client to make the login request
    const result = await apiClient.login({ email, password });

    if (result.success && result.data?.token) {
      // Store the session data
      storeSession(result.data.user, result.data.token);
      return { success: true, user: result.data.user };
    }

    return { success: false, error: result.error || 'Login failed' };
  } catch (error) {
    return { success: false, error: 'An error occurred during login' };
  }
};

export const signUp = async (email: string, password: string, name?: string) => {
  try {
    // Use our API client to make the registration request
    const result = await apiClient.register({ email, password, name });

    if (result.success && result.data?.token) {
      // Store the session data
      storeSession(result.data.user, result.data.token);
      return { success: true, user: result.data.user };
    }

    return { success: false, error: result.error || 'Registration failed' };
  } catch (error) {
    return { success: false, error: 'An error occurred during registration' };
  }
};

export const signOut = async () => {
  try {
    // Clear the session data
    clearSession();
    return { success: true };
  } catch (error) {
    return { success: false, error: 'An error occurred during logout' };
  }
};

// Check if user is authenticated
export const isAuthenticated = () => {
  return isValidSession();
};

// Refresh session if needed
export const refreshSession = () => {
  const session = getSession();
  if (session) {
    // Update the timestamp to extend the session
    const updatedSession = {
      ...session,
      timestamp: Date.now(),
    };
    localStorage.setItem(SESSION_KEY, JSON.stringify(updatedSession));
    apiClient.setToken(session.token);
  }
};