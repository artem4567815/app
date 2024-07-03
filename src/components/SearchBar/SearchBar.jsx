import React, { useState } from 'react';

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
      <input
        type="text"
        value={gameName}
        onChange={handleChange}
        placeholder="Enter game name"
      />
      <button type="submit">Search</button>
    </form>
  );
}

export default SearchBar;
