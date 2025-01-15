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
		res.status(HttpStatusCode.OK).json({
			message: "Stand trends",
			data
		});
	} catch (error) {
		res.status(HttpStatusCode.INTERNAL_SERVER_ERROR).json({
			message: "Internal server error",
			error
		});
	}
	
};

export const mlController = { getStandTrends };