import React, { useState } from 'react';
import SearchBar from './components/SearchBar/SearchBar';
import GameList from './components/GameList/GameList';
import './App.css';


function App() {
    const [games, setGames] = useState([]);

    const handleSearch = async (gameName) => {
        const response = await fetch('/search', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({ game_name: gameName })
        });
        const data = await response.json();
        setGames(data);
  };

    return (
    <div className="App">
        <SearchBar onSearch={handleSearch} />
        <GameList games={games} />
    </div>
    );
}

export default App;
