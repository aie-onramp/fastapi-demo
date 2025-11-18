import React from 'react';
import './DataTable.css';

/**
 * Reusable data table component.
 *
 * @param {Object} props
 * @param {Array} props.data - Array of objects to display
 * @param {Array} props.columns - Column definitions [{key, label, render?}]
 * @param {Function} props.onRowClick - Optional row click handler
 */
export default function DataTable({ data, columns, onRowClick }) {
  if (!data || data.length === 0) {
    return <div className="empty-table">No data available</div>;
  }

  return (
    <div className="data-table-container">
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col.key}>{col.label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr
              key={row.id || index}
              onClick={() => onRowClick && onRowClick(row)}
              className={onRowClick ? 'clickable' : ''}
            >
              {columns.map((col) => (
                <td key={col.key}>
                  {col.render ? col.render(row[col.key], row) : row[col.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
