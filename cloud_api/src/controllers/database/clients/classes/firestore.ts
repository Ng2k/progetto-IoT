/**
 * @fileoverview Interfaccia per i clienti del database
 * @author Nicola Guerra <nicola.ng2k@gmail.com>
 * @author Tommaso Mortara <>
*/
import { firestore } from "../../../../firebase/app";

import type { IClient } from "../interfaces/client.interface";

/**
 * @class Firestore
 * @implements {IClient}
 * @description Classe per la gestione del database Firestore
 */
export class Firestore implements IClient {
	/**
	 * Funzione per ottenere un microcontrollore tramite il suo id
	 * @param {string} id - Id del microcontrollore 
	 * @returns {Promise<any>} Ritorna il microcontrollore
	 */
	private async getMicrocontrollerById(id: string): Promise<any> {
		const collection = firestore.collection('Microcontrollers');
		const docRef = collection.doc(id);

		// Faccio query di select per documento mc -> {id, current_stand_id, is_busy}
		const doc = await docRef.get();

		if (!doc.exists) {
			console.log('No such document!');
			return null;
		}

		return doc.data();
	}
	
	/**
	 * Funzione per ottenere uno stand tramite il suo riferimento
	 * @param {any} reference - Riferimento al documento dello stand 
	 * @returns {Promise<any>} Ritorna il documento dello stand
	 */
	private async getStandByReference(reference: any): Promise<any> {
		const currentStandDoc = await reference.get();
		
		if (!currentStandDoc.exists) {
			console.log('No such document for current_stand!');
			return null;
		}

		const currentStandData = currentStandDoc.data();
		currentStandData.id = currentStandDoc.id;
		return currentStandData;
	}

	async updateReadings(readings: any): Promise<any> {
		//todo aggiungi readings a Firestore
		const dataToUpload = await Promise.all(
			readings.map(async (reading: any) => {
				const data = await this.getMicrocontrollerById(reading.mc_id);
				const currentStand = (data && data.current_stand)
					? await this.getStandByReference(data.current_stand)
					: {};
				currentStand.metadata = reading
				return currentStand;
			})
		);

		dataToUpload.forEach(({ id, metadata }: any) => {
			const standRef = firestore.collection('Stands').doc(id);
			try {
				standRef.update({ metadata });
			} catch (error) {
				console.error('Error adding document: ', error);
			}
		});
	}
}
