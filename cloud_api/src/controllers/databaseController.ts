/**
 * @fileoverview Interfaccia per i clienti del database
 * @author Nicola Guerra <nicola.ng2k@gmail.com>
 * @author Tommaso Mortara <>
*/
import type { Request, Response } from "express";

import { DatabaseHandler } from "./database/databaseHandler";
import { Firestore } from "./database/clients/";
import { HttpStatusCode } from "../http-status-code";

/**
 * Funzione per caricare le readings nel database
 * @param {Request} req 
 * @param {Response} res 
 */
const uploadReadings = async (req: Request, res: Response) => {
	const { readings } = req.body;
	const database: DatabaseHandler = new DatabaseHandler(
		new Firestore(),
	);

	try {
		const temp = await database.uploadReadings(readings);
		res.status(HttpStatusCode.OK).json({
			message: "Readings uploaded",
			data: temp
		});
	} catch (error) {
		res.status(HttpStatusCode.INTERNAL_SERVER_ERROR).json({
			message: "Internal server error"
		});
	}
};

const controller = {
	uploadReadings,
};

export const databaseController = controller;