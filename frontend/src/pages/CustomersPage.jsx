import React, { useState, useEffect } from 'react';
import { fetchCustomers, searchCustomer, updateCustomer } from '../api';
import DataTable from '../components/DataTable';
import SearchBar from '../components/SearchBar';
import './CustomersPage.css';

/**
 * Customers page component.
 *
 * Displays all customers with search and edit functionality.
 */
export default function CustomersPage() {
  const [customers, setCustomers] = useState([]);
  const [filteredCustomers, setFilteredCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingId, setEditingId] = useState(null);
  const [editForm, setEditForm] = useState({ email: '', phone: '' });

  // Load customers on mount
  useEffect(() => {
    loadCustomers();
  }, []);

  const loadCustomers = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchCustomers();
      setCustomers(data);
      setFilteredCustomers(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (query) => {
    if (!query.trim()) {
      setFilteredCustomers(customers);
      return;
    }

    const lowercaseQuery = query.toLowerCase();
    const filtered = customers.filter(
      (customer) =>
        customer.name.toLowerCase().includes(lowercaseQuery) ||
        customer.email.toLowerCase().includes(lowercaseQuery) ||
        customer.phone.includes(query) ||
        customer.username.toLowerCase().includes(lowercaseQuery)
    );
    setFilteredCustomers(filtered);
  };

  const startEdit = (customer) => {
    setEditingId(customer.id);
    setEditForm({
      email: customer.email,
      phone: customer.phone,
    });
  };

  const cancelEdit = () => {
    setEditingId(null);
    setEditForm({ email: '', phone: '' });
  };

  const saveEdit = async (customerId) => {
    try {
      await updateCustomer(customerId, editForm);
      await loadCustomers(); // Reload to show updated data
      setEditingId(null);
      setEditForm({ email: '', phone: '' });
    } catch (err) {
      setError(err.message);
    }
  };

  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'name', label: 'Name' },
    {
      key: 'email',
      label: 'Email',
      render: (value, row) => {
        if (editingId === row.id) {
          return (
            <input
              type="email"
              value={editForm.email}
              onChange={(e) =>
                setEditForm({ ...editForm, email: e.target.value })
              }
              className="edit-input"
            />
          );
        }
        return value;
      },
    },
    {
      key: 'phone',
      label: 'Phone',
      render: (value, row) => {
        if (editingId === row.id) {
          return (
            <input
              type="tel"
              value={editForm.phone}
              onChange={(e) =>
                setEditForm({ ...editForm, phone: e.target.value })
              }
              className="edit-input"
              pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}"
            />
          );
        }
        return value;
      },
    },
    { key: 'username', label: 'Username' },
    {
      key: 'actions',
      label: 'Actions',
      render: (_, row) => {
        if (editingId === row.id) {
          return (
            <div className="action-buttons">
              <button onClick={() => saveEdit(row.id)} className="btn-save">
                Save
              </button>
              <button onClick={cancelEdit} className="btn-cancel">
                Cancel
              </button>
            </div>
          );
        }
        return (
          <button onClick={() => startEdit(row)} className="btn-edit">
            Edit
          </button>
        );
      },
    },
  ];

  if (loading) {
    return (
      <div className="customers-page">
        <div className="container">
          <h1>Customers</h1>
          <div className="loading">Loading customers...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="customers-page">
      <div className="container">
        <h1>Customer Management</h1>

        {error && <div className="error">{error}</div>}

        <div className="page-header">
          <p>Total customers: {customers.length}</p>
          <SearchBar
            onSearch={handleSearch}
            placeholder="Search by name, email, phone, or username..."
          />
        </div>

        <DataTable data={filteredCustomers} columns={columns} />
      </div>
    </div>
  );
}
