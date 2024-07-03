import React from 'react';

function GameCard({ game }) {
  return (
    <div className="card">
      <div className="card-body">
        <h5 className="card-title">{game.name}</h5>
        <p className="card-text">Steam: ${game.steam_price}</p>
        <p className="card-text">Epic: ${game.epic_price}</p>
        <a href={game.details_url} className="btn btn-primary">Details</a>
      </div>
    </div>
  );
}

export default GameCard;
