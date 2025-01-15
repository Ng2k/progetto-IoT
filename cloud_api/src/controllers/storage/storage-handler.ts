/**
 * @fileoverview Classe per la gestione dello storage
 * @author Nicola Guerra <nicola.ng2k@gmail.com>
 * @author Tommaso Mortara <>
*/
import type { IStorageClient } from "./clients/interfaces/storage-client.interface";

export class StorageHandler {
	constructor(private readonly _client: IStorageClient) { }

	/**
	 * Funzione per calcolare trend con ml/ai
	 * @returns {Promise<object>} - Trend degli stand dell'evento calcolato dal modello di ML/AI
	 */
	async getStandTrends(): Promise<object[]> {
		return await this._client.getStandTrends();
	}
}