/**
 * @fileoverview Route per modello machine learning
 * @author Nicola Guerra <nicola.ng2k@gmail.com>
 * @author Tommaso Mortara <>
*/
import { Router } from "express";
import { mlController } from "../controllers";

const router = Router();

router.get("/get-stand-trends", mlController.getStandTrends);

export const mlRouter = router;