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
               'Try asking: "Look up customer with email john@example.com"',
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
          <h3>Example queries:</h3>
          <ul>
            <li onClick={() => setInput('Look up customer with email john@example.com')}>
              Look up customer with email john@example.com
            </li>
            <li onClick={() => setInput('Show me their orders')}>
              Show me their orders
            </li>
            <li onClick={() => setInput('Cancel order 47652')}>
              Cancel order 47652
            </li>
            <li onClick={() => setInput('Update customer 1213210 email to newemail@example.com')}>
              Update customer email address
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
