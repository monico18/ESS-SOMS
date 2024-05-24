import express from "express";
import passport from "passport";
import user from "../controllers/user.controller.js";
import { checkBlacklist, getUserFromToken } from "../auth.js";

const router = express.Router();

router.post('/register', user.register);
router.post('/login', user.login);
router.get('/profile', passport.authenticate('jwt', { session: false }), checkBlacklist, getUserFromToken, user.profile);
router.delete('/profile', passport.authenticate('jwt', { session: false }), checkBlacklist, getUserFromToken, user.deleteUser);
router.put('/profile/password', passport.authenticate('jwt', { session: false }), checkBlacklist, getUserFromToken, user.changePassword);
router.post('/logout', passport.authenticate('jwt', { session: false }), checkBlacklist, getUserFromToken, user.logout);

export default router;