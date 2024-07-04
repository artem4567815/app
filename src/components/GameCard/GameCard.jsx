import React from 'react';
import './GameCard.css'

function GameCard({ game }) {
  return (
    <div className="search-cards">
      <div className="search-product-card">
        <img className="search-product-image" src={game.img} alt="Фото игры" />
        <h2 className="search-product-name">{game.name}</h2>
        <p className="search-product-price">Steam: {game.steam_price}</p>
        <p className="search-product-price">Epic: {game.epic_price}</p>
        <a href={game.details_url} className="search-buy-button">Details</a>
        <p className="search-rating">рейтинг</p>
    </div>
  </div>
  );
}

export default GameCard;
