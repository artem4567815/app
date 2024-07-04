import React from 'react';
import './NavPanel.module.css'


function NavPanel() {
    return (
        <div className="search-navigation-panel">
            <a className="search-link" href="/store">ИЗБРАННОЕ</a>
            <a className="search-link" href="/">ГЛАВНАЯ</a>
            <a className="search-chosen-link" href="/catalog">О НАС</a>
        </div>
    );
}

export default NavPanel;
