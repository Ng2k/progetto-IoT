/**
 * @fileoverview API for cloud services
 * @package cloud_api
 * @version 0.0.1
 * @author Nicola Guerra <nicola.ng2k@gmail.com>
 * @author Tommaso Mortara <>
*/
import express from "express";

import { databaseRouter } from "./routers"

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use("/database", databaseRouter)
app.all("*", (req, res) => {
	res.status(404).json({ message: "Route not found" });
});

app.listen(port, () => {
	console.log(`Server is running on port ${port}`);
});
