import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ChatPage from './pages/ChatPage';
import './App.css';

/**
 * Main App component with routing.
 *
 * For MVP, only the Chat page is implemented.
 * Customer and Order pages will be added in Phase 4 and 5.
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
            <li className="coming-soon">
              <span>Customers (Coming Soon)</span>
            </li>
            <li className="coming-soon">
              <span>Orders (Coming Soon)</span>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/" element={<ChatPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
