import React from 'react';
import GameCard from '../GameCard/GameCard';

function GameList({ games }) {
  return (
    <div className="game-list">
      {games.map((game) => {
        return <GameCard game={game[0]} />
      })}
    </div>
  );
}

export default GameList;
