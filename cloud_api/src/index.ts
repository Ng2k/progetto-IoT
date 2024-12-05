/**
 * @fileoverview API for cloud services
 * @package cloud_api
 * @version 0.0.1
*/
import express from "express";

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
//app.use();
app.all("*", (req, res) => {
	res.status(404).json({ message: "Route not found" });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
