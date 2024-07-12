import React, { useState, useEffect } from 'react';
import '../GameCard/GameCard.css'

function Favorites() {
    const [favorites, setFavorites] = useState([]);

    useEffect(() => {
        const fetchFavorites = async () => {
            const response = await fetch('http://localhost:5000/favorites', {
                method: 'GET',
                headers: {
                'Content-Type': 'application/json'
                },
            });
            const data = await response.json();
            setFavorites(data)
            console.log(data);
        };
    
        fetchFavorites();
      }, []);

    return (
        <div className="search-cards">
            {favorites.map((game, index) => (
                <div className="search-cards">
                    <div className="search-product-card">
                        <img className="search-product-image" src={game.img} alt="Фото игры" />
                        <h2 className="search-product-name">{game.name }</h2>
                        <p className="search-product-price"><a className="link" href={game.steam_url}>{!game.price ? "Steam: Not Found" : "Steam: " + game.price }</a></p>
                        <p className="search-product-price"><a className="link" href={game.epic_url}>{!game.epic_price ? "Epic: Not Found" : "Epic: " + game.epic_price }</a></p>
                    </div>
                </div>
            ))}
        </div>
    );
}

export default Favorites;
