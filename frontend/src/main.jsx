import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import ParentDashboard from './components/ParentDashboard';
import './index.css';

const Home = () => (
  <div className="flex justify-center items-center h-full">
    <h1 className="text-4xl font-bold">Welcome to Bravolino!</h1>
  </div>
);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<ParentDashboard />} />
        </Routes>
      </Layout>
    </Router>
  </React.StrictMode>
);
