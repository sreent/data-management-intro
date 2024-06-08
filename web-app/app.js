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
// Route for the first research question
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

// Add similar routes for the other research questions
// ...

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
