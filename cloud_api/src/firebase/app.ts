/**
 * @fileoverview Configurazione di Firebase
 * @author Nicola Guerra <nicola.ng2k@gmail.com>
 * @author Tommaso Mortara <>
*/

import admin from "firebase-admin";
import type { ServiceAccount } from "firebase-admin";
import serviceAccount from "./firebase.json";

const app = admin.initializeApp({
	credential: admin.credential.cert(serviceAccount as ServiceAccount)
});

export const firestore = app.firestore();
