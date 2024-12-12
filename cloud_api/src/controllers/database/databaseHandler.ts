/**
 * @fileoverview Classe per la gestione del database
 * @author Nicola Guerra <nicola.ng2k@gmail.com>
 * @author Tommaso Mortara <>
*/
import type { IClient } from "./clients/";

export class DatabaseHandler {
	constructor(private readonly _client: IClient) { }

	async uploadReadings(readings: any): Promise<any> {
		return this._client.updateReadings(readings);
	}

	async getStandsOccupancy(eventId: string): Promise<any> {
		return this._client.getStandsOccupancy(eventId);
	}

	async getCurrentEvent(masterId: string): Promise<any> {
		return this._client.getCurrentEvent(masterId);
	}
}