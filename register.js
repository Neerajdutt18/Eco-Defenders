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
  database: "mydatabase",
});

// Connect to MySQL database
connection.connect((err) => {
  if (err) throw err;
  console.log("Connected to MySQL database");
});

app.get("/", (req, res) => {
  res.sendFile(__dirname + "/register.html");
});

// Handle form submission
app.post("/submit", (req, res) => {
  const { name, email, username, password, role } = req.body;

  // Check if username or email already exists
  const checkSql = "SELECT * FROM register WHERE username = ? OR email = ?";
  connection.query(checkSql, [username, email], (err, result) => {
    if (err) {
      console.error("Error checking username or email:", err);
      res.status(500).send("Error processing your submission");
    } else if (result.length > 0) {
      // Username or email already exists
      const existingUser = result[0];
      if (existingUser.username === username) {
        res.status(400).send("Username is already taken");
      } else {
        res.status(400).send("Email is already registered");
      }
    } else {
      // Insert submitted data into MySQL database
      const sql =
        "INSERT INTO register (name, email, username, password, role) VALUES (?, ?, ?, ?, ?)";
      connection.query(
        sql,
        [name, email, username, password, role],
        (err, result) => {
          if (err) {
            console.error("Error inserting submission into database:", err);
            res.status(500).send("Error processing your submission");
          } else {
            console.log("Submission inserted into database:", result);
            res.redirect("/login.html");
          }
        }
      );
    }
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
