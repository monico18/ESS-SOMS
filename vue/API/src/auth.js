import jwt from 'jsonwebtoken';
import models from './models/index.js';
let jwtBlacklist = {};

export const addToBlacklist = (token) => {
    jwtBlacklist[token] = true;
};

export const checkBlacklist = (req, res, next) => {
    const token = req.headers.authorization.split(' ')[1];
    if (jwtBlacklist[token]) {
        return res.status(401).json({ message: 'Token is no longer valid' });
    }
    next();
};

export const getUserFromToken = async (req, res, next) => {
    try {
        const token = req.headers.authorization.split(' ')[1];
        const payload = jwt.verify(token, process.env.JWT_SECRET);
        const userRecord = await models.user.findOne({ where: { id: payload.id } });
        req.user = userRecord;
        next();
    } catch (error) {
        next(error);
    }
};