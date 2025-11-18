# Blackbird Frontend

React frontend for the Blackbird Customer Support Application.

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Backend server running on http://localhost:8000

### Setup

1. **Install dependencies**:
```bash
cd frontend
npm install
```

2. **Start development server**:
```bash
npm run dev
```

The app will be available at: http://localhost:5173

## Project Structure

```
frontend/
├── src/
│   ├── App.jsx              # Main app component with routing
│   ├── api.js               # Backend API wrapper functions
│   ├── pages/
│   │   ├── ChatPage.jsx     # AI chat interface
│   │   ├── CustomersPage.jsx   # Customer management
│   │   └── OrdersPage.jsx   # Order management
│   └── components/
│       ├── ChatMessage.jsx  # Chat message display
│       ├── DataTable.jsx    # Reusable data table
│       └── SearchBar.jsx    # Search input component
├── index.html               # HTML entry point
├── package.json             # Dependencies and scripts
├── vite.config.js           # Vite configuration (proxy to backend)
└── README.md
```

## Available Scripts

### `npm run dev`
Starts the development server with hot reload.
- Opens at: http://localhost:5173
- Proxies API requests to backend at http://localhost:8000

### `npm run build`
Builds the app for production to `dist/` folder.

### `npm run preview`
Preview the production build locally.

### `npm run lint`
Runs ESLint to check code quality.

## Features

### Chat Page (`/`)
- AI-powered customer support chat
- Interact with Claude to:
  - Look up customers by email/phone/username
  - View customer orders
  - Cancel orders (if Processing status)
  - Update customer contact info

**Example queries**:
- "Look up customer with email john@example.com"
- "Show me their orders"
- "Cancel order 47652"

### Customers Page (`/customers`)
- View all customers in a table
- Search by email, phone, or username
- Edit customer contact information inline
- View customer's orders

### Orders Page (`/orders`)
- View all orders in a table
- Filter by status (Processing, Shipped, Delivered, Cancelled)
- Cancel orders (only if status = Processing)
- View order details

## API Integration

The frontend communicates with the FastAPI backend via:

**Base URL**: http://localhost:8000/api (configured in `vite.config.js` proxy)

**Endpoints**:
- `POST /chat` - Send chat messages
- `GET /customers` - Fetch all customers
- `POST /customers/search` - Search customers
- `PATCH /customers/{id}` - Update customer
- `GET /orders` - Fetch all orders
- `PATCH /orders/{id}/cancel` - Cancel order

See [backend/README.md](../backend/README.md) for full API documentation.

## Development

### Hot Reload
Changes to `.jsx` files trigger automatic browser refresh.

### Browser DevTools
Press F12 to open browser developer tools for debugging.

### Network Inspection
Check the "Network" tab in DevTools to see API requests/responses.

### React DevTools
Install the React DevTools browser extension for component debugging:
- [Chrome](https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi)
- [Firefox](https://addons.mozilla.org/en-US/firefox/addon/react-devtools/)

## Component Architecture

### Pages
- **Stateful components** that manage data fetching and business logic
- Use React Router for navigation
- Call backend API via `api.js` functions

### Components
- **Reusable UI components** used across multiple pages
- Accept props for customization
- No direct API calls (data passed from pages)

Example component usage:
```jsx
// In CustomersPage.jsx
<DataTable
  data={customers}
  columns={['name', 'email', 'phone']}
  onEdit={handleEditCustomer}
/>
```

## Troubleshooting

### Port 5173 already in use
```bash
# Kill the process using port 5173
lsof -ti:5173 | xargs kill -9

# Or use a different port
npm run dev -- --port 3000
```

### Backend connection errors
1. Verify backend is running: `curl http://localhost:8000/api/health`
2. Check proxy configuration in `vite.config.js`
3. Check browser console for CORS errors

### Module not found errors
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### React hooks errors
- Make sure you're using React 18+
- Check that hooks are called at the top level of components
- Verify component names start with uppercase letter

## Styling

This project uses basic CSS for simplicity (educational prototype).

To add styles:
1. Create a `.css` file in `src/`
2. Import it in your component: `import './MyComponent.css'`

Example:
```css
/* src/ChatPage.css */
.chat-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
```

## Resources

- [React Documentation](https://react.dev/)
- [Vite Guide](https://vitejs.dev/guide/)
- [React Router](https://reactrouter.com/en/main)
- [MDN Web Docs](https://developer.mozilla.org/en-US/)
