import React, { useState } from 'react';
import './SearchBar.css'

function SearchBar({ onSearch }) {
  const [gameName, setGameName] = useState('');

  const handleChange = (e) => {
    setGameName(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(gameName);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="container justify-content-center">
        <div className="row">
            <div className="col-md-8">
                <div className="input-group mb-3">
                  <input type="text" value={gameName} onChange={handleChange} className="form-control input-text" placeholder="Search products...." aria-label="Recipient's username" aria-describedby="basic-addon2" />
                  <div className="input-group-append">
                      <button className="btn btn-outline-warning btn-lg" type="submit"><i className="fa fa-search"></i></button>
                  </div>
                </div>
            </div>        
        </div>
    </div>
  </form>
  );
}

export default SearchBar;
