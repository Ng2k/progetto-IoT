/**
 * @author Nicola Guerra <nicola.ng2k@gmail.com>
 * @author Tommaso Mortara <>
*/
import { supabase } from "../../../../supabase/app";
import type { IStorageClient } from "../interfaces/storage-client.interface";

/**
 * @class SupabaseStorage
 * @implements {IStorageClient}
 * @description Classe per la gestione dello storage di Supabase
 */
export class SupabaseStorage implements IStorageClient {
	async getStandTrends(): Promise<object> {
		const bucket = process.env.SUPABASE_BUCKET || "";
		const file = process.env.DATABASE_EXPORT_CSV || "";

		const { data, error } = await supabase.storage.from(bucket).download(file);
		if (error) {
			console.error(error);
			throw error;
		}

		const csv = await data.text() || "";
		const trends = this.csvToObject(csv);
		
		return trends;
	}

	/**
	 * @function csvToObject
	 * @description Trasforma un CSV in un oggetto TypeScript
	 * @param {string} csv - Il CSV da trasformare
	 * @returns {object[]} - L'array di oggetti risultante
	 */
	private csvToObject(csv: string): object[] {
		const lines = csv.split("\n");
		if (lines.length === 0) return [];
	
		const headers = lines[0].split(",").map(header => header.trim().replace(/^"|"$/g, ''));
		const result = lines.slice(1).map(line => {
			const values = line.match(/(".*?"|[^",\s]+)(?=\s*,|\s*$)/g)?.map(value => value.trim().replace(/^"|"$/g, '')) || [];
			const obj: any = {};
			headers.forEach((header, index) => {
				try {
					obj[header] = (header === "readings") ? JSON.parse(values[index].replace(/""/g, '"')) : values[index];
				} catch (error) {
					console.error(`Error parsing value for header ${header}:`, error);
					obj[header] = values[index];
				}
			});
			return obj;
		});
		return result;
	}
}