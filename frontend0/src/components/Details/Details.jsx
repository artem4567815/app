import React, { useState, useEffect  } from 'react';
import { useParams } from 'react-router-dom';
import "./Details.css"

function Details() {
    const [game_data, setGameData] = useState(null);
    const { gameName } = useParams();
    const [countries, setCountries] = useState([]);
    const [country, setCountry] = useState('');
    const [prices, setPrices] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const fetchGameDetails = async () => {
            setLoading(true)
            const response = await fetch(`http://localhost:5000/details/${gameName}`, {
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/json'
                  }
            })
            const data = await response.json(); 
            setLoading(false)
            console.log(data)
            setGameData(data);
        };
    
        fetchGameDetails();

      }, [gameName]);
    
      useEffect(() => {
        async function Fetching() {
            const response = await fetch('http://localhost:5000/countries', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
            });
            const data = await response.json();
            setCountries(data)
            console.log(data);
          }
  
          Fetching()
      }, []);
  
      const handleCountryChange = (e) => {
          setCountry(e.target.value);
      };
  
      useEffect(() => {
        if (country) {
          async function Fetching() {
            const response = await fetch(`http://localhost:5000/prices/${gameName}/${country}`, {
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/json'
                  },
            });
            const data = await response.json();
            setPrices(data)
            console.log(data);
          }
  
          Fetching()
        }
      }, [country]);

      const addToFavorites = async (gameName) => {
        const response = await fetch(`http://localhost:5000/add_favorites`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ game_name: gameName })
        });
      }
      

  return (
    <div>
      {game_data ? (
        <div className='info'>
          <img className="img" src={game_data.img} alt="game" />
          <div className='data'>
            <div className='info'>
              <h4>Review: {game_data.review ? game_data.review.toFixed(2) : "100"}%</h4>
              <h4 className='playtime'>Playtime: {game_data.playtime}h</h4>
            </div>
            <h5>Description: {game_data.description}</h5>
            <h6><button onClick={() => addToFavorites(gameName)} className='favorites'>Add To Favorites</button></h6>
          </div>
        </div>
      ) : (
        <div className="overlay"><div className="loader"></div></div>
      )}
      <div className='GamePrice'>
        <label>
            <select value={country} onChange={handleCountryChange}>
                <option value="">Select Country</option>
                {countries.map((country) => (
                    <option className='card' key={country} value={country}>{country}</option>
                ))}
            </select>
        </label>
        {prices ? (
          "current_price" in prices ? (
            <table>
              <thead>
                <tr>
                  <th>Country</th>
                  <th>Current Price</th>
                  <th>Initial Price</th>
                  <th>Discount</th>
                  <th>Currency</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>{country}</td>
                  <td>{prices.current_price}</td>
                  <td>{prices.initial_price}</td>
                  <td>{prices.discount}%</td>
                  <td>{prices.currency}</td>
                </tr>
              </tbody>
            </table>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Country</th>
                  <th>Current Price</th>
                  <th>Initial Price</th>
                  <th>Discount</th>
                  <th>Currency</th>
                  <th>Platform</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>{country}</td>
                  <td>{prices.current_price_steam}</td>
                  <td>{prices.initial_price_steam}</td>
                  <td>{prices.discount_steam}%</td>
                  <td>{prices.currency_steam}</td>
                  <td>{"Steam"}</td>
                </tr>
                <tr>
                  <td>{country}</td>
                  <td>{prices.current_price_epic}</td>
                  <td>{prices.initial_price_epic}</td>
                  <td>{prices.discount_epic}%</td>
                  <td>{prices.currency_epic}</td>
                  <td>{"Epic Store"}</td>
                </tr>
              </tbody>
            </table>
          )
        ) : (<p></p>)
        }
        
      </div>
    </div>
  );
}

export default Details;