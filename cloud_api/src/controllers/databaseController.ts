import type { Request, Response, NextFunction } from "express";
import { DatabaseHandler } from "./database/databaseHandler";
import { Firestore } from "./database/clients/";

const controller = {
	uploadReadings: async (req: Request, res: Response, next: NextFunction) => {
		// todo: logica di upload readings

		//prendere dal body della request i dati da inserire nel db
		const { readings } = req.body;
		//preprocessare i dati se necessario
		//inserire i dati nel db
		const database: DatabaseHandler = new DatabaseHandler(
			new Firestore(),

		);

		try {
			const temp = await database.uploadReadings(readings);
		} catch (error) {
			res.status(500).json({ message: "Internal server error" });
			next();
		}

		res.status(200).json({ message: "Database route" });
	}
};

export const databaseController = controller;