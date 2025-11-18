import React, { useState, useEffect } from 'react';
import { fetchOrders, cancelOrder } from '../api';
import DataTable from '../components/DataTable';
import './OrdersPage.css';

/**
 * Orders page component.
 *
 * Displays all orders with status filtering and cancellation functionality.
 */
export default function OrdersPage() {
  const [orders, setOrders] = useState([]);
  const [filteredOrders, setFilteredOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [statusFilter, setStatusFilter] = useState('');

  // Load orders on mount
  useEffect(() => {
    loadOrders();
  }, []);

  const loadOrders = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchOrders();
      setOrders(data);
      setFilteredOrders(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusFilter = (status) => {
    setStatusFilter(status);
    if (!status) {
      setFilteredOrders(orders);
    } else {
      const filtered = orders.filter((order) => order.status === status);
      setFilteredOrders(filtered);
    }
  };

  const handleCancelOrder = async (orderId) => {
    if (!window.confirm(`Are you sure you want to cancel order ${orderId}?`)) {
      return;
    }

    setError(null);
    setSuccess(null);

    try {
      const result = await cancelOrder(orderId);
      setSuccess(result.message);
      await loadOrders(); // Reload to show updated status

      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError(err.message);
    }
  };

  const getStatusBadge = (status) => {
    const statusClass = `status-badge status-${status.toLowerCase()}`;
    return <span className={statusClass}>{status}</span>;
  };

  const columns = [
    { key: 'id', label: 'Order ID' },
    { key: 'customer_id', label: 'Customer ID' },
    { key: 'product', label: 'Product' },
    { key: 'quantity', label: 'Qty' },
    {
      key: 'price',
      label: 'Price',
      render: (value) => `$${value.toFixed(2)}`,
    },
    {
      key: 'status',
      label: 'Status',
      render: (value) => getStatusBadge(value),
    },
    {
      key: 'actions',
      label: 'Actions',
      render: (_, row) => {
        if (row.status === 'Processing') {
          return (
            <button
              onClick={() => handleCancelOrder(row.id)}
              className="btn-cancel-order"
            >
              Cancel
            </button>
          );
        }
        return <span className="no-action">—</span>;
      },
    },
  ];

  if (loading) {
    return (
      <div className="orders-page">
        <div className="container">
          <h1>Orders</h1>
          <div className="loading">Loading orders...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="orders-page">
      <div className="container">
        <h1>Order Management</h1>

        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}

        <div className="page-header">
          <p>
            Total orders: {orders.length}
            {statusFilter && ` (Filtered: ${filteredOrders.length})`}
          </p>

          <div className="filter-section">
            <label htmlFor="status-filter">Filter by status:</label>
            <select
              id="status-filter"
              value={statusFilter}
              onChange={(e) => handleStatusFilter(e.target.value)}
              className="status-filter"
            >
              <option value="">All Statuses</option>
              <option value="Processing">Processing</option>
              <option value="Shipped">Shipped</option>
              <option value="Delivered">Delivered</option>
              <option value="Cancelled">Cancelled</option>
            </select>
          </div>
        </div>

        <DataTable data={filteredOrders} columns={columns} />

        <div className="info-box">
          <strong>Note:</strong> Only orders with "Processing" status can be cancelled.
          Orders that are Shipped, Delivered, or already Cancelled cannot be modified.
        </div>
      </div>
    </div>
  );
}
