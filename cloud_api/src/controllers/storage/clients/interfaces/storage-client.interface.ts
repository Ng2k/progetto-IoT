/**
 * @fileoverview Interfaccia per i clienti del servizio di storage file
 * @author Nicola Guerra <nicola.ng2k@gmail.com>
 * @author Tommaso Mortara <>
*/

/**
 * @interface IStorageClient
 * @description Interfaccia per i clienti dello storage file
 */
export interface IStorageClient {
	/**
	 * @method downloadFile
	 * @description Metodo per scaricare un file dallo storage
	 * @returns {Promise<object>} - Trend degli stand dell'evento calcolato dal modello di ML/AI
	 */
	getStandTrends(): Promise<object>;
}