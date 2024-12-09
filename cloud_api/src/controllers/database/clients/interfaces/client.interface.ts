/**
 * @fileoverview Interfaccia per i clienti del database
 * @author Nicola Guerra <nicola.ng2k@gmail.com>
 * @author Tommaso Mortara <>
*/

/**
 * @interface IClient
 * @description Interfaccia per i clienti del database
 */
export interface IClient {
	/**
	 * Funzione per aggiungere rilevazioni al database
	 * @param {any} readings - Rilevazioni
	 * @throws {Error} - Se non è possibile aggiungere le rilevazioni
	 */
	updateReadings(readings: any): Promise<any>;

	/**
	 * Funzione per ottenere il numero di persone per ogni stand di un evento
	 * @param {string} eventId - Id dell'evento
	 * @returns {Promise<any>} Ritorna il numero di persone per ogni stand
	 */
	getStandsOccupancy(eventId: string): Promise<any>;
}