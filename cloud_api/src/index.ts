/**
 * @fileoverview API for cloud services
 * @package cloud_api
 * @version 0.0.1
 * @author Nicola Guerra <nicola.ng2k@gmail.com>
 * @author Tommaso Mortara <>
*/
import express from "express";

import { databaseRouter, mlRouter } from "./routers"
import { HttpStatusCode } from "./http-status-code";

const app = express();
const port = parseInt(process.env.PORT || "") || 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use("/database", databaseRouter);
app.use("/ml-model", mlRouter);
app.all("*", (req, res) => {
	res.status(HttpStatusCode.NOT_FOUND).json({ message: "Route not found" });
});

app.listen(port, '0.0.0.0', () => {
	console.log(`Server is running on port ${port}`);
});
