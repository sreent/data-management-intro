const express = require('express');
const mysql = require('mysql');
const bodyParser = require('body-parser');
const mustacheExpress = require('mustache-express');
const dotenv = require('dotenv').config();

const app = express();

// Set up Mustache as the view engine
app.engine('mustache', mustacheExpress());
app.set('view engine', 'mustache');
app.set('views', __dirname + '/views');

// Serve static files from the "public" directory
app.use(express.static('public'));

// Use body-parser middleware to parse request bodies
app.use(bodyParser.urlencoded({ extended: true }));

// Set up database connection
const db = mysql.createConnection({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASS,
  database: process.env.DB_NAME
});

db.connect(err => {
  if (err) {
    console.error('Error connecting to the database:', err);
    return;
  }
  console.log('Connected to the database.');
});

// Serve the main page
app.get('/', (req, res) => {
  res.render('index');
});

// Define routes for each research question
app.get('/city-rankings', (req, res) => {
  const query = 'SELECT city_name, AVG(aqi_value) AS average_aqi FROM pollutions JOIN cities ON pollutions.city_id = cities.city_id GROUP BY city_name ORDER BY average_aqi DESC';
  db.query(query, (err, results) => {
    if (err) {
      console.error('Error fetching city rankings:', err);
      res.status(500).send('Error fetching data');
      return;
    }
    res.render('city-rankings', { rankings: results });
  });
});

app.get('/national-urban-aq', (req, res) => {
  const query = 'SELECT country_name, AVG(aqi_value) AS average_aqi FROM pollutions JOIN cities ON pollutions.city_id = cities.city_id JOIN countries ON cities.country_id = countries.country_id GROUP BY country_name ORDER BY average_aqi';
  db.query(query, (err, results) => {
    if (err) {
      console.error('Error fetching national urban air quality:', err);
      res.status(500).send('Error fetching data');
      return;
    }
    res.render('national-urban-aq', { countries: results });
  });
});

app.get('/dominant-pollutants', (req, res) => {
  const query = 'SELECT pollutant_name, AVG(aqi_value) AS average_aqi FROM pollutions JOIN pollutants ON pollutions.pollutant_id = pollutants.pollutant_id GROUP BY pollutant_name ORDER BY average_aqi DESC';
  db.query(query, (err, results) => {
    if (err) {
      console.error('Error fetching dominant pollutants:', err);
      res.status(500).send('Error fetching data');
      return;
    }
    res.render('dominant-pollutants', { pollutants: results });
  });
});

app.get('/pollutant-prevalence', (req, res) => {
  const query = 'SELECT city_name FROM cities WHERE EXISTS (SELECT * FROM pollutions p1 JOIN pollutants pol1 ON p1.pollutant_id = pol1.pollutant_id AND pol1.pollutant_name = "NO2" WHERE p1.city_id = cities.city_id AND p1.aqi_value > (SELECT p2.aqi_value FROM pollutions p2 JOIN pollutants pol2 ON p2.pollutant_id = pol2.pollutant_id AND pol2.pollutant_name = "CO" WHERE p2.city_id = cities.city_id))';
  db.query(query, (err, results) => {
    if (err) {
      console.error('Error fetching pollutant prevalence:', err);
      res.status(500).send('Error fetching data');
      return;
    }
    res.render('pollutant-prevalence', { cities: results });
  });
});

app.get('/urban-centers-profile', (req, res) => {
  const query = 'SELECT city_name, pollutant_name, AVG(aqi_value) AS average_aqi FROM pollutions JOIN cities ON pollutions.city_id = cities.city_id JOIN pollutants ON pollutions.pollutant_id = pollutants.pollutant_id GROUP BY city_name, pollutant_name HAVING AVG(aqi_value) > (SELECT AVG(aqi_value) FROM pollutions) ORDER BY average_aqi DESC';
  db.query(query, (err, results) => {
    if (err) {
      console.error('Error fetching pollution profiles of urban centers:', err);
      res.status(500).send('Error fetching data');
      return;
    }
    res.render('urban-centers-profile', { profiles: results });
  });
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
