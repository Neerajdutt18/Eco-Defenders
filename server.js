const express = require("express");
const mysql = require("mysql");
const bodyParser = require("body-parser");
const ejs = require("ejs");

const app = express();
const port = 5500;

// Set up view engine
app.set("view engine", "ejs");
app.set("views", __dirname + "/views");

// Use body-parser middleware to parse request bodies
app.use(bodyParser.urlencoded({ extended: true }));

// Serve static files
app.use("/img", express.static("static/"));
app.use("/css", express.static("css"));
app.use("/js", express.static("js"));
app.use("/webfonts", express.static("webfonts"));

// Create connection to MySQL database
const connection = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "9596",
  database: "myDatabase",
});

// Connect to MySQL database
connection.connect(function (error) {
  if (error) throw error;
  else console.log("Connected successfully");
});

// Serve the HTML files
app.get("/", (req, res) => {
  res.sendFile(__dirname + "/front.html");
});

app.get("/login.html", (req, res) => {
  res.sendFile(__dirname + "/login.html");
});
app.get("/register.html", (req, res) => {
  res.sendFile(__dirname + "/register.html");
});
app.get("/certified.html", (req, res) => {
  res.sendFile(__dirname + "/certified.html");
});

app.get("/index", (req, res) => {
  res.sendFile(__dirname + "/index.html");
});
app.get("/about.html", (req, res) => {
  res.sendFile(__dirname + "/about.html");
});

app.get("/service.html", (req, res) => {
  res.sendFile(__dirname + "/service.html");
});

app.get("/pickup.html", (req, res) => {
  res.sendFile(__dirname + "/pickup.html");
});

app.get("/admin", (req, res) => {
  res.sendFile(__dirname + "/admin.html");
});

app.get("/educate.html", (req, res) => {
  res.sendFile(__dirname + "/educate.html");
});

app.get("/waste.html", (req, res) => {
  res.sendFile(__dirname + "/waste.html");
});

// Handle form submissions
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
app.post("/submit-certificate", (req, res) => {
  const { FullName, mobileNumber, address } = req.body;

  // Insert submitted data into MySQL database
  const sql =
    "INSERT INTO certificates (FullName, mobileNumber, address) VALUES (?, ?, ?)";
  connection.query(sql, [FullName, mobileNumber, address], (err, result) => {
    if (err) {
      console.error("Error inserting certificate into database:", err);
      res.status(500).send("Error processing your certificate request");
    } else {
      console.log("Certificate request inserted into database:", result);
      res.send("Thank you for submitting your certificate request!");
    }
  });
});

app.post("/takepickup", bodyParser.urlencoded(), (req, res) => {
  const {
    name,
    email,
    phone,
    waste_type,
    quantity,
    date_pickup,
    time_pickup,
    address_pickup,
  } = req.body;

  // Insert submitted data into MySQL database
  const sql =
    "INSERT INTO takepickup (name, email, phone, waste_type, quantity, date_pickup, time_pickup, address_pickup) VALUES (?, ?, ?, ?, ?, ?, ?, ?)";
  connection.query(
    sql,
    [
      name,
      email,
      phone,
      waste_type,
      quantity,
      date_pickup,
      time_pickup,
      address_pickup,
    ],
    (err, result) => {
      if (err) {
        console.error("Error inserting pickup into database:", err);
        res.status(500).send("Error processing your pickup request");
      } else {
        console.log("Pickup request inserted into database:", result);
        res.send("Thank you for scheduling a pickup!");
      }
    }
  );
});

// pickup
app.post("/pickup", bodyParser.urlencoded(), (req, res) => {
  const {
    name,
    email,
    phone,
    waste_type,
    quantity,
    date_pickup,
    time_pickup,
    address_pickup,
  } = req.body;

  // Insert submitted data into MySQL database
  const sql =
    "INSERT INTO takepickup (name, email, phone, waste_type, quantity, date_pickup, time_pickup, address_pickup) VALUES (?, ?, ?, ?, ?, ?, ?, ?)";
  connection.query(
    sql,
    [
      name,
      email,
      phone,
      waste_type,
      quantity,
      date_pickup,
      time_pickup,
      address_pickup,
    ],
    (err, result) => {
      if (err) {
        console.error("Error inserting pickup into database:", err);
        res.status(500).send("Error processing your pickup request");
      } else {
        console.log("Pickup request inserted into database:", result);
        res.send("Thank you for scheduling a pickup!");
      }
    }
  );
});

// Handle login form submission
app.post("/login", bodyParser.urlencoded(), (req, res) => {
  var username = req.body.username;
  var email = req.body.email;
  var password = req.body.password;

  connection.query(
    "SELECT * FROM Users WHERE username=? AND email = ? AND password = ?",
    [username, email, password],
    function (error, results, fields) {
      if (results.length > 0) {
        // If login successful, check the role
        var role = results[0].role;
        if (role === "user") {
          // If role is user, redirect to index.html
          res.redirect("/index");
        } else if (role === "admin") {
          // If role is admin, redirect to admin.html
          res.redirect("/admin");
        }
      } else {
        // If login failed, redirect back to login page
        res.redirect("/login.html?error=No+user+exists");
      }
      res.end();
    }
  );
});

// Handle register form submission
app.post("/register", bodyParser.urlencoded(), (req, res) => {
  const { name, email, username, password, role } = req.body;

  // Check if username or email already exists
  const checkSql = "SELECT * FROM Users WHERE username = ? OR email = ?";
  connection.query(checkSql, [username, email], (err, result) => {
    if (err) {
      console.error("Error checking username or email:", err);
      res.status(500).send("Error processing your submission");
    } else if (result.length > 0) {
      // Username or email already exists
      const existingUser = result[0];
      if (existingUser.username === username) {
        res.redirect("/register.html?error=Username is already taken");
      } else {
        res.redirect("/register.html?error=Email is already registered");
      }
    } else {
      // Insert submitted data into MySQL database
      const sql =
        "INSERT INTO Users (name, email, username, password, role) VALUES (?, ?, ?, ?, ?)";
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
