import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

export default function Listings() {
  const [listings, setListings] = useState([]);

  useEffect(() => {
    axios.get('/api/listings/')
      .then(res => setListings(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h1 className="text-xl font-semibold mb-3">Alle Angebote</h1>
      <ul className="space-y-2">
        {listings.map(l => (
          <li key={l.id}>
            <Link to={`/listing/${l.id}`} className="text-blue-600 hover:underline">
              {l.title} – €{l.price}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
