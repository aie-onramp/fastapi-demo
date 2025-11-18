import React from 'react';
import './ChatMessage.css';

/**
 * Chat message component.
 *
 * Displays a single message in the chat interface.
 *
 * @param {Object} props
 * @param {string} props.role - 'user' or 'assistant'
 * @param {string} props.content - Message text
 * @param {Array} [props.toolCalls] - Optional tool calls (for assistant messages)
 */
export default function ChatMessage({ role, content, toolCalls }) {
  return (
    <div className={`chat-message ${role}`}>
      <div className="message-header">
        <strong>{role === 'user' ? 'You' : 'AI Assistant'}</strong>
      </div>
      <div className="message-content">
        {content}
      </div>
      {toolCalls && toolCalls.length > 0 && (
        <details className="tool-calls">
          <summary>Tools used ({toolCalls.length})</summary>
          <ul>
            {toolCalls.map((call, index) => (
              <li key={index}>
                <strong>{call.tool}</strong>
                <pre>{JSON.stringify(call.input, null, 2)}</pre>
              </li>
            ))}
          </ul>
        </details>
      )}
    </div>
  );
}
