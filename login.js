const mysql = require("mysql");
const express = require("express");
const bodyParser = require("body-parser");
const encoder = bodyParser.urlencoded();

const app = express();
app.use("/img", express.static("static/"));
app.use("/css", express.static("css"));
app.use("/js", express.static("js"));
app.use("/webfonts", express.static("webfonts"));

const connection = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "9596",
  database: "myDatabase",
});

connection.connect(function (error) {
  if (error) throw error;
  else console.log("Connected successfully");
});

// Serve front.html initially
app.get("/", function (req, res) {
  res.sendFile(__dirname + "/front.html");
});

// Serve login.html
app.get("/login.html", function (req, res) {
  res.sendFile(__dirname + "/login.html");
});

// Handle login form submission
app.post("/", encoder, function (req, res) {
  var username = req.body.username;
  var email = req.body.email;
  var password = req.body.password;

  connection.query(
    "SELECT * FROM Users WHERE username=? AND email = ? AND password = ?",
    [username, email, password],
    function (error, results, fields) {
      if (results.length > 0) {
        // If login successful, redirect to index.html
        res.redirect("/index");
      } else {
        // If login failed, redirect back to login page
        res.redirect("/login");
      }
      res.end();
    }
  );
});

// Serve index.html
app.get("/index", function (req, res) {
  res.sendFile(__dirname + "/index.html");
});

// Serve service.html
app.get("/service.html", function (req, res) {
  res.sendFile(__dirname + "/service.html");
});
app.get("/pickup.html", function (req, res) {
  res.sendFile(__dirname + "/pickup.html");
});
app.get("/educate.html", function (req, res) {
  res.sendFile(__dirname + "/educate.html");
});

app.listen(5500, function () {
  console.log("Server is running on port 5500");
});
