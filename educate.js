const express = require("express");
const mysql = require("mysql");
const bodyParser = require("body-parser"); // Import body-parser middleware

const app = express();
const port = 4000;

// Use body-parser middleware to parse request bodies
app.use(bodyParser.urlencoded({ extended: true }));

// Create connection to MySQL database
const connection = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "9596",
  database: "educate",
});

// Connect to MySQL database
connection.connect((err) => {
  if (err) throw err;
  console.log("Connected to MySQL database");
});

// Serve the HTML file
app.get("/", (req, res) => {
  res.sendFile(__dirname + "/educate.html");
});

// Handle form submission
app.post("/submit", (req, res) => {
  const { blog, image, video } = req.body;

  // Insert submitted data into MySQL database
  const sql = "INSERT INTO submissions (blog, image, video) VALUES (?, ?, ?)";
  connection.query(sql, [blog, image, video], (err, result) => {
    if (err) {
      console.error("Error inserting submission into database:", err);
      res.status(500).send("Error processing your submission");
    } else {
      console.log("Submission inserted into database:", result);
      res.send("Thank you for your contribution!");
    }
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
