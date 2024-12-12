/**
 * @fileoverview Route per database
 * @author Nicola Guerra <nicola.ng2k@gmail.com>
 * @author Tommaso Mortara <>
*/
import { Router } from "express";
import { databaseController } from "../controllers";

const router = Router();

router.get("/events/:event/get-stands-occupancy", databaseController.getStandsOccupancy);
router.get("/events/get-current-event", databaseController.getCurrentEvent);

router.post("/upload-readings", databaseController.uploadReadings);

export const databaseRouter = router;