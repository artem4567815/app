import React, { useState } from 'react';
import SearchBar from './components/SearchBar/SearchBar';
import GameList from './components/GameList/GameList';
import NavPanel from './components/NavPanel/NavPanel';
import './App.css';


function App() {
    const [games, setGames] = useState([]);

    const handleSearch = async (gameName) => {
        const response = await fetch('http://localhost:5000/search', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({ game_name: gameName })
        });
        console.log(response)
        const data = await response.json();
        console.log(data);
        setGames(data);
  };

    return (
    <div className="App">
        <NavPanel />
        <SearchBar onSearch={handleSearch} />
        <GameList games={games} />
    </div>
    );
}

export default App;
