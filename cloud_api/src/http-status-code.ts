/**
 * @fileoverview Enumerazione per i codici di stato HTTP
 * @author Nicola Guerra <nicola.ng2k@gmail.com>
 * @author Tommaso Mortara <>
*/

/**
 * @enum HttpStatusCode
 * @description Enumerazione per i codici di stato HTTP
 */
export enum HttpStatusCode {
	OK = 200,
	BAD_REQUEST = 400,
	UNAUTHORIZED = 401,
	FORBIDDEN = 403,
	NOT_FOUND = 404,
	INTERNAL_SERVER_ERROR = 500
}