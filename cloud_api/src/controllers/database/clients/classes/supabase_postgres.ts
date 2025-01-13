/**
 * @fileoverview Interfaccia per i clienti del database
 * @author Nicola Guerra <nicola.ng2k@gmail.com>
 * @author Tommaso Mortara <>
*/
import { supabase } from "../../../../supabase/app";
import type { IClient } from "../interfaces/client.interface";

/**
 * @class SupabasePostgres
 * @implements {IClient}
 * @description Classe per la gestione del database Postgres di Supabase
 */
export class SupabasePostgres implements IClient {
	/**
	 * Funzione per creare un oggetto con le readings raggruppati per id microcontrollore
	 * @param readings - Lista di readings
	 * @returns {{ [key: string]: any[] }} readings raggruppate
	 */
	private createStandGroups(readings: any): { [key: string]: any[] } {
		return readings.reduce((acc: any, reading: any) => {
			const { mc_id } = reading;
			if (!acc[mc_id]) acc[mc_id] = [];
			delete reading.mc_id;
			acc[mc_id].push(reading);
			return acc;
		}, {});
	}

	async updateReadings(readings: any): Promise<any> {
		const standGroups = this.createStandGroups(readings);
		const keys = Object.keys(standGroups);
		keys.forEach(async (key) => {
			const { data: lastReadings, error: errorSelect } = await supabase
				.from("Stands")
				.select("readings")
				.filter("mc_id", "eq", key);

			if (errorSelect) {
				console.error("Errore:", errorSelect.message);
				return null;
			}

			const [{ readings }] = lastReadings;

			if(!readings) return null;

			const { data, error } = await supabase
				.from("Stands")
				.update({
					readings: readings.concat(standGroups[key])
				})
				.filter("mc_id", "eq", key);
			
			if (error) {
				console.error("Errore:", error.message);
				return null;
			}
		});

		return standGroups;
	}

	async getStandsOccupancy(eventId: string): Promise<any> {
		const { data, error } = await supabase
			.from("Stands")
			.select("name, readings")
			.filter("event_id", "eq", eventId);

		if (error) {
			console.error("Errore:", error.message);
			return null;
		}

		return data.reduce((acc: { [key: string]: any }, e) => {
			if(e.name) acc[e.name] = e.readings[e.readings.length - 1].people;
			return acc;
		}, {});
	}

	async getCurrentEvent(masterId: string): Promise<any> {
		const { data, error } = await supabase
			.from("Microprocessors")
			.select("event_id")
			.filter("mp_id", "eq", masterId);

		if (error) {
			console.error("Errore:", error.message);
			return null;
		} else {
			console.log("Dati:", data);
			return data;
		}
	}
}