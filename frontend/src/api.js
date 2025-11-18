/**
 * API wrapper for backend communication.
 *
 * All API calls go through Vite proxy to http://localhost:8000/api
 */

const API_BASE = '/api';

/**
 * Send a chat message to Claude AI.
 *
 * @param {string} message - User's message
 * @returns {Promise<Object>} - Response with {response, tool_calls}
 */
export async function sendChatMessage(message) {
  const response = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to send message');
  }

  return response.json();
}

/**
 * Get all customers.
 *
 * @returns {Promise<Array>} - List of customers
 */
export async function fetchCustomers() {
  const response = await fetch(`${API_BASE}/customers`);

  if (!response.ok) {
    throw new Error('Failed to fetch customers');
  }

  return response.json();
}

/**
 * Search for a customer.
 *
 * @param {string} key - Search field (email, phone, username)
 * @param {string} value - Search value
 * @returns {Promise<Object>} - Customer object
 */
export async function searchCustomer(key, value) {
  const response = await fetch(`${API_BASE}/customers/search`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ key, value }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Customer not found');
  }

  return response.json();
}

/**
 * Update customer contact information.
 *
 * @param {string} customerId - Customer ID
 * @param {Object} updates - Updates object {email?, phone?}
 * @returns {Promise<Object>} - Updated customer
 */
export async function updateCustomer(customerId, updates) {
  const response = await fetch(`${API_BASE}/customers/${customerId}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(updates),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to update customer');
  }

  return response.json();
}

/**
 * Get all orders, optionally filtered by status.
 *
 * @param {string} [status] - Filter by status (Processing, Shipped, Delivered, Cancelled)
 * @returns {Promise<Array>} - List of orders
 */
export async function fetchOrders(status = null) {
  const url = status
    ? `${API_BASE}/orders?status=${encodeURIComponent(status)}`
    : `${API_BASE}/orders`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error('Failed to fetch orders');
  }

  return response.json();
}

/**
 * Cancel an order.
 *
 * @param {string} orderId - Order ID
 * @returns {Promise<Object>} - Cancellation result {success, message}
 */
export async function cancelOrder(orderId) {
  const response = await fetch(`${API_BASE}/orders/${orderId}/cancel`, {
    method: 'PATCH',
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to cancel order');
  }

  return response.json();
}
