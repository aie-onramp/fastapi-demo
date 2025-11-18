import React, { useState, useRef, useEffect } from 'react';
import { sendChatMessage } from '../api';
import ChatMessage from '../components/ChatMessage';
import './ChatPage.css';

/**
 * Chat page component.
 *
 * AI-powered customer support chat interface.
 * Users can ask the AI assistant to look up customers, view orders, cancel orders, etc.
 */
export default function ChatPage() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello! I\'m your AI customer support assistant. I can help you:\n\n' +
               '• Look up customers by email, phone, or username\n' +
               '• View customer orders\n' +
               '• Cancel orders (if they\'re still processing)\n' +
               '• Update customer contact information\n\n' +
               'Try one of the example queries below, or ask me anything about our customers and orders!',
      toolCalls: []
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!input.trim() || isLoading) {
      return;
    }

    const userMessage = input.trim();
    setInput('');
    setError(null);

    // Add user message to chat
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      // Send to backend
      const response = await sendChatMessage(userMessage);

      // Add assistant response to chat
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: response.response,
          toolCalls: response.tool_calls || []
        }
      ]);
    } catch (err) {
      setError(err.message);
      // Add error message to chat
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: `Error: ${err.message}`,
          toolCalls: []
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-page">
      <div className="container">
        <h1>AI Customer Support Chat</h1>

        {error && (
          <div className="error">
            <strong>Error:</strong> {error}
          </div>
        )}

        <div className="chat-container">
          <div className="messages">
            {messages.map((msg, index) => (
              <ChatMessage
                key={index}
                role={msg.role}
                content={msg.content}
                toolCalls={msg.toolCalls}
              />
            ))}
            {isLoading && (
              <div className="loading-indicator">
                <div className="spinner"></div>
                <span>AI is thinking...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form onSubmit={handleSubmit} className="chat-input-form">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message... (e.g., 'Look up customer with email john@example.com')"
              disabled={isLoading}
              className="chat-input"
            />
            <button type="submit" disabled={isLoading || !input.trim()}>
              Send
            </button>
          </form>
        </div>

        <div className="example-queries">
          <h3>Example queries (click to try):</h3>
          <ul>
            <li onClick={() => setInput('Can you confirm my username? My email is meilin@gmail.com.')}>
              Can you confirm my username? My email is meilin@gmail.com.
            </li>
            <li onClick={() => setInput('Can you send me a list of my recent orders? My phone number is 222-333-4444.')}>
              Can you send me a list of my recent orders? My phone number is 222-333-4444.
            </li>
            <li onClick={() => setInput('I need to confirm my current user info and order status. My username is liamn.')}>
              I need to confirm my current user info and order status. My username is liamn.
            </li>
            <li onClick={() => setInput("I'm checking on the status of an order, the order id is 74651.")}>
              I'm checking on the status of an order, the order id is 74651.
            </li>
            <li onClick={() => setInput('I need to cancel Order ID 97531.')}>
              I need to cancel Order ID 97531.
            </li>
            <li onClick={() => setInput('I lost my phone and need to update my contact information. My user id is 1213210.')}>
              I lost my phone and need to update my contact info. My user id is 1213210.
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
