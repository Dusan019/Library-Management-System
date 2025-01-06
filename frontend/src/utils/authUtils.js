// src/utils/authUtils.js
export function parseJwt(token) {
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const decodedData = JSON.parse(atob(base64));
      return decodedData;
    } catch (error) {
      console.error('Error decoding token:', error);
      return null;
    }
  }
  
  export function isTokenExpired(token) {
    const decodedToken = parseJwt(token);
    if (!decodedToken) return true;
  
    const currentTime = Date.now() / 1000; // Current time in seconds
    return decodedToken.exp < currentTime;
  }
  
  export function startPeriodicTokenCheck(onLogout, interval = 60000) {
    const checkTokenValidity = () => {
      const token = localStorage.getItem('token');
      if (token && isTokenExpired(token)) {
        alert('Your session has expired. Please log in again.');
        localStorage.removeItem('token');
        onLogout();
      }
    };
  
    const intervalId = setInterval(checkTokenValidity, interval);
    return intervalId; // Return the interval ID to clear it later
  }
  