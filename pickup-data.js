app.get("/pickup-data", (req, res) => {
  // Fetch data from the takepickup table
  const sql = "SELECT * FROM takepickup";
  connection.query(sql, (err, results) => {
    if (err) {
      console.error("Error fetching pickup data:", err);
      res.status(500).send("Error fetching pickup data");
    } else {
      // Render the pickup-data view and pass the results to it
      res.render("pickup-data", { pickupData: results });
    }
  });
});
