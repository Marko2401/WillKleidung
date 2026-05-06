import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import Listings from './pages/Listings';

export default function App() {
  return (
    <div className="p-4">
      <header className="mb-4">
        <Link to="/" className="text-2xl font-bold">
          WillKleidung (React)
        </Link>
      </header>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/listings" element={<Listings />} />
      </Routes>
    </div>
  );
}
