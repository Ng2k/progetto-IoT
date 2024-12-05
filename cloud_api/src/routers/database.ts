/**
 * @fileoverview Route per database
 * @author Nicola Guerra <nicola.ng2k@gmail.com>
 * @author Tommaso Mortara <>
*/
import { Router } from "express";
import { databaseController } from "../controllers";

const router = Router();

router.post("/upload-readings", databaseController.uploadReadings);

export const databaseRouter = router;