/**
 * @fileoverview Interfaccia per i clienti del database
 * @author Nicola Guerra <nicola.ng2k@gmail.com>
 * @author Tommaso Mortara <>
*/
import type { Request, Response } from "express";

import { StorageHandler } from "./storage/storage-handler";
import { SupabaseStorage } from "./storage/clients/classes/supabase-storage";
import { HttpStatusCode } from "../http-status-code";

/**
 * Funzione per ottenere le tendenze di ogni singolo stand basandosi su tipologia, storico e altri dati.
 * @param {Request} req 
 * @param {Response} res 
 */
const getStandTrends = async (req: Request, res: Response) => {
	/*
		3 - formattare contenuto
		4 - elaborare output
		5 - inviare output
	*/
	const storage = new StorageHandler(new SupabaseStorage());
	try {
		const data = await storage.getStandTrends();
		const threshold = 5;
		const margin = 1;

		res.status(HttpStatusCode.OK).json({
			message: "Stand trends",
			data: data.reduce((acc: any, curr: any) => {
				const { stand_name: name, readings } = curr;

				const peopleAvg = readings.reduce((acc: number, curr: any) => {
					const { people } = curr;
					return acc + people;
				}, 0) / readings.length;
	
				if(peopleAvg > threshold + margin) acc[name] = +1;
				else if(peopleAvg < threshold - margin) acc[name] = -1;
				else acc[name] = 0;
	
				return acc;
			}, {})
		});
	} catch (error) {
		res.status(HttpStatusCode.INTERNAL_SERVER_ERROR).json({
			message: "Internal server error",
			error
		});
	}
	
};

export const mlController = { getStandTrends };