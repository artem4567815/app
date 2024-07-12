import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import SearchBar from './components/SearchBar/SearchBar'
import GameList from './components/GameList/GameList';
import Details from './components/Details/Details';
import Favorites from './components/Favorites/Favorites';
import './App.css';


function App() {
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedPage, setSelectPage] = useState(2);

    const handleSearch = async (gameName) => {
        setLoading(true)
        const response = await fetch(`http://localhost:5000/search/${gameName}`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              //body: JSON.stringify({ game_name: gameName })
        });
        const data = await response.json();
        const gamesWithIds = data.map((game, index) => ({ ...game, id: index.toString() }));
        setLoading(false)
        console.log(data);
        setGames(gamesWithIds);
    };
    const handlePageClick = (page) => {
      setSelectPage(page);
    };
    return (
      <Router>
        <div className="App">
          <div className="search-navigation-panel">
            <Link onClick={() => handlePageClick(1)} className={selectedPage === 1 ? 'search-link highlight' : 'search-link'} to="/store">ИЗБРАННОЕ</Link>
            <Link onClick={() => handlePageClick(2)} className={selectedPage === 2 ? 'search-link highlight' : 'search-link'} to="/">ГЛАВНАЯ</Link>
          </div>
            
          <Routes>
            <Route path="/" element={ 
                <React.Fragment>
                  <SearchBar onSearch={handleSearch} />
                  {loading && <div className="overlay"><div className="loader"></div></div>}
                  {games && <GameList games={games} />};
                </React.Fragment>}
              >
            </Route>
            <Route path="/store" element={<Favorites /> } />
            <Route path="/details/:gameName" element={<Details />} />
          </Routes>
        </div>
      </Router>
    );
}

export default App;
