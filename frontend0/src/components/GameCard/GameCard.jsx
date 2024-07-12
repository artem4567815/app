import React from 'react';
import { Link } from 'react-router-dom';
import './GameCard.css'

function GameCard({ game }) {
  return (
    <div className="search-cards">
      <div className="search-product-card">
        <img className="search-product-image" src={game.img} alt="Фото игры" />
        <h2 className="search-product-name">{game.name }</h2>
        <p className="search-product-price"><a className="link" href={game.steam_url}>{!game.price ? "Steam: Not Found" : "Steam: " + game.price }</a></p>
        <p className="search-product-price"><a className="link" href={game.epic_url}>{!game.epic_price ? "Epic: Not Found" : "Epic: " + game.epic_price }</a></p>
        <Link to={`/details/${game.name}`} className="btn btn-primary">Details</Link>
    </div>
  </div>
  );
}

export default GameCard;
