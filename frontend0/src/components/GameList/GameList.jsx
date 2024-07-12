import React from 'react';
import GameCard from '../GameCard/GameCard';
import './GameList.css'
function GameList({ games }) {
  return (
    <div className="game-list">
      {games.map((game) => {
        return  <GameCard key={game.name} game={game} />
      })}
    </div>
  );
}

export default GameList;
