/**
 * @fileoverview Interfaccia per i clienti del database
 * @author Nicola Guerra <nicola.ng2k@gmail.com>
 * @author Tommaso Mortara <>
*/
import { firestore } from "../../../../firebase/app";

import type {
	DocumentReference,
	DocumentData,
	DocumentSnapshot
} from "firebase-admin/firestore";
import type { IClient } from "../interfaces/client.interface";

/**
 * @class Firestore
 * @implements {IClient}
 * @description Classe per la gestione del database Firestore
 */
export class Firestore implements IClient {
	/**
	 * Funzione per creare un oggetto con le readings raggruppati per id microcontrollore
	 * @param readings - Lista di readings
	 * @returns {{ [key: string]: any[] }} readings raggruppate
	 */
	private createStandGroups(readings: any): { [key: string]: any[] } {
		return readings.reduce((acc: any, reading: any) => {
			const { mc_id } = reading;
			if (!acc[mc_id]) acc[mc_id] = [];
			acc[mc_id].push(reading);
			return acc;
		}, {});
	}
	/**
	 * Funzione per ottenere un microcontrollore tramite il suo id
	 * @param {string} id - Id del microcontrollore 
	 * @returns {Promise<any>} Ritorna il microcontrollore
	 */
	private async getMicrocontrollerById(id: string): Promise<{
		id: string,
		data: FirebaseFirestore.DocumentData | undefined
	} | null> {
		const collection = firestore.collection('Microcontrollers');
		const docRef = collection.doc(id);
		const doc = await docRef.get();

		if (!doc.exists) {
			console.log('No such document!');
			return null;
		}

		return {
			id: doc.id,
			data: doc.data()
		};
	}

	async updateReadings(readings: any): Promise<any> {
		const readingsGrouped: { [key: string]: any[] } = this.createStandGroups(readings);
		return await Promise.all(
			Object
				.keys(readingsGrouped)
				.map(this.getMicrocontrollerById)
				.map(async mcPromise => {
					const mc = await mcPromise;
					if(!(mc && mc.data && mc.id)) {
						return null;
					}

					const readings = readingsGrouped[mc.id];
					const currentStand: DocumentReference = mc.data.current_stand
					const standSnapshot: DocumentSnapshot = await currentStand.get();
					const stand: DocumentData|undefined = standSnapshot.data();
					if (!standSnapshot.exists || !stand) {
						console.log('No such document!');
						return null
					}
					const metadata = stand.metadata.concat(readings);
					//todo: controllo se non sto inserende la stessa reading due volte
					//currentStand.update({ metadata });
					return readings;
				})
		);
	}
}
