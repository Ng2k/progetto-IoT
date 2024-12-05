import type { IClient } from "./clients/";

export class DatabaseHandler {
	constructor(private readonly _client: IClient) { }

	async uploadReadings(readings: any): Promise<void> {
		this._client.updateReadings(readings);
	}
}