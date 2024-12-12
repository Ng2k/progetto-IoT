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
 * Funzione per ottenere l'evento corrente
 * @param {Request} req - richiesta
 * @param {Response} res - risposta
 */
const getCurrentEvent = async (req: Request, res: Response) => {
	const bridge = req.query["mp-master-id"] as string || "";
	const database: DatabaseHandler = new DatabaseHandler(
		new Firestore(),
	);

	try {
		const data = await database.getCurrentEvent(bridge);
		res.status(HttpStatusCode.OK).json({
			message: "Current event",
			data
		});
	} catch (error) {
		res.status(HttpStatusCode.INTERNAL_SERVER_ERROR).json({
			message: "Internal server error"
		});
	}
};

/**
 * Funzione per ottenere il numero di persone per ogni stand di un evento
 * @param {Request} req 
 * @param {Response} res 
 */
const getStandsOccupancy = async (req: Request, res: Response) => {
	const { event } = req.params;
	const database: DatabaseHandler = new DatabaseHandler(
		new Firestore(),
	);

	try {
		const data = await database.getStandsOccupancy(event);
		res.status(HttpStatusCode.OK).json({
			message: "Stands occupancy",
			data
		});
	} catch (error) {
		res.status(HttpStatusCode.INTERNAL_SERVER_ERROR).json({
			message: "Internal server error"
		});
	}
};

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
		const { event, uploaded_readings } = await database.uploadReadings(readings);
		res.status(HttpStatusCode.OK).json({
			message: "Readings uploaded",
			event, 
			data: uploaded_readings
		});
	} catch (error) {
		console.log(error);
		res.status(HttpStatusCode.INTERNAL_SERVER_ERROR).json({
			message: "Internal server error"
		});
	}
};

export const databaseController = {
	uploadReadings,
	getStandsOccupancy,
	getCurrentEvent
};