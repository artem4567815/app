import React from 'react';
import GameCard from '../GameCard/GameCard';

function GameList({ games }) {
  return (
    <div className="game-list">
      {games.map((game) => (
        <GameCard game={game} />
      ))}
    </div>
  );
}

export default GameList;
