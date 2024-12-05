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
	updateReadings(readings: any): void;
}