const express = require("express");
const bodyParser = require("body-parser");
const session = require("express-session");

const app = express();
const port = 5500; // Make sure it's the same port you're listening on

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(
  session({
    secret: "secret",
    resave: false,
    saveUninitialized: true,
  })
);

let users = [];

// Login endpoint
app.post("/login", (req, res) => {
  const { username, password } = req.body;

  // Check credentials
  const user = users.find(
    (user) => user.username === username && user.password === password
  );
  if (user) {
    req.session.isLoggedIn = true;
    res.status(200).send("Login successful");
  } else {
    res.status(401).send("Invalid username or password");
  }
});

// Registration endpoint
app.post("/register", (req, res) => {
  const { newUsername, newPassword } = req.body;

  // Check if username already exists
  const existingUser = users.find((user) => user.username === newUsername);
  if (existingUser) {
    res.status(400).send("Username already exists");
  } else {
    users.push({ username: newUsername, password: newPassword });
    res.status(201).send("Registration successful");
  }
});

// Service endpoint
app.get("/service", (req, res) => {
  if (req.session.isLoggedIn) {
    res.status(200).send("Welcome to the service!");
  } else {
    res.redirect("/");
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://127.0.0.1:5500/c.html`);
});
