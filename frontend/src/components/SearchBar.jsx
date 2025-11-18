import React from 'react';
import './SearchBar.css';

/**
 * Search bar component for filtering data.
 *
 * @param {Object} props
 * @param {Function} props.onSearch - Callback when search is submitted
 * @param {string} props.placeholder - Placeholder text
 */
export default function SearchBar({ onSearch, placeholder = 'Search...' }) {
  const [query, setQuery] = React.useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form onSubmit={handleSubmit} className="search-bar">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder={placeholder}
        className="search-input"
      />
      <button type="submit" className="search-button">
        Search
      </button>
      {query && (
        <button
          type="button"
          onClick={() => {
            setQuery('');
            onSearch('');
          }}
          className="clear-button"
        >
          Clear
        </button>
      )}
    </form>
  );
}
