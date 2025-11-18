import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ChatPage from './pages/ChatPage';
import CustomersPage from './pages/CustomersPage';
import OrdersPage from './pages/OrdersPage';
import './App.css';

/**
 * Main App component with routing.
 *
 * Includes all three main pages:
 * - Chat: AI-powered customer support interface
 * - Customers: Customer data management
 * - Orders: Order management and tracking
 */
function App() {
  return (
    <Router>
      <div className="app">
        <nav>
          <ul>
            <li>
              <Link to="/">AI Chat</Link>
            </li>
            <li>
              <Link to="/customers">Customers</Link>
            </li>
            <li>
              <Link to="/orders">Orders</Link>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/" element={<ChatPage />} />
          <Route path="/customers" element={<CustomersPage />} />
          <Route path="/orders" element={<OrdersPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
