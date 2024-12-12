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
		data: FirebaseFirestore.DocumentData | undefined,
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

	async getStandsOccupancy(eventId: string): Promise<any> {
		const eventRef = firestore.collection('Events').doc(eventId);
		const mcRef = firestore.collection('Microcontrollers');
		const mcCollection = mcRef.where('current_event', '==', eventRef);
		const mcList = await mcCollection.get();
		const mcListData = mcList.docs.map(doc => doc.data());
		const standListPromise = mcListData.map(async mc => {
			const currentStand = await mc.current_stand.get();
			return {
				id: currentStand.id,
				...currentStand.data()
			}
		});
		const standListData = await Promise.all(standListPromise);
		const standsOccupancy = standListData.reduce((acc: { [key: string]: number }, stand: any) => {
			return {
				...acc,
				[stand.id]: stand.metadata[stand.metadata.length - 1].people
			};
		}, {});
		return standsOccupancy;	
	}

	async updateReadings(readings: any): Promise<any> {
		const readingsGrouped: { [key: string]: any[] } = this.createStandGroups(readings);
		const mcIdList = Object.keys(readingsGrouped);
		const mcList = mcIdList.map(this.getMicrocontrollerById);
		const firstMc = await mcList[0];
		if(!firstMc || !firstMc.data || !firstMc.data.current_event) {
			return null;
		}
		const eventDocument = await firstMc.data.current_event.get();
		const event = eventDocument.data();
		const uploaded_readings = mcList.map(async mcPromise => {
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
			currentStand.update({ metadata });
			return {
				event,
				uploaded_readings: metadata
			};
		});

		const output = (await Promise.all(uploaded_readings))[0];
		return output;
	}

	async getCurrentEvent(masterId: string): Promise<any> {
		const bridgeRef = firestore
			.collection("Microprocessors")
			.doc(masterId);

		const eventCollection = firestore
			.collection("Events")
			.where("microprocessor", "==", bridgeRef);
		
		const eventList = await eventCollection.get();
		const [ eventRef ] = eventList.docs;
		const currentEvent = eventRef.id;

		return {
			id: currentEvent,
			...eventRef.data()
		};
	}
}
