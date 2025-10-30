import React from 'react';
import ReactDOM from 'react-dom/client';

import App from './App';
import '@styles/global.css';
import '@fullcalendar/common/main.css';
import '@fullcalendar/daygrid/main.css';
import '@fullcalendar/timegrid/main.css';
import 'frappe-gantt/dist/frappe-gantt.css';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
